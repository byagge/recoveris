#!/usr/bin/env python3
"""Build complete static mirror under main/ from _pages/full/*.html."""
from __future__ import annotations

import re
import urllib.parse
from pathlib import Path

ROOT = Path(r"d:\codes\recoveris.io")
FULL = ROOT / "_pages" / "full"
MAIN = ROOT / "main"
IMG = MAIN / "images"
CSS = MAIN / "css"
JS = MAIN / "js"
FONTS = MAIN / "fonts"

ALIAS_REDIRECTS = {
    "asset-recovery": "digital-asset-recovery",
    "investigations": "blockchain-investigations",
    "intelligence": "blockchain-investigation-management-system",
}


def list_local(folder: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not folder.exists():
        return out
    for p in folder.iterdir():
        if p.is_file():
            out[p.name.lower()] = p.name
    return out


LOCAL_CSS = list_local(CSS)
LOCAL_JS = list_local(JS)
LOCAL_IMG = list_local(IMG)
LOCAL_FONTS = list_local(FONTS)

# Known site paths (filled after reading urls)
SITE_PATHS: set[str] = set()


def stem_candidates(name: str) -> list[str]:
    name = urllib.parse.unquote(name)
    cands = [name]
    if "-scaled." in name:
        cands.append(name.replace("-scaled.", "."))
    stem, _, ext = name.rpartition(".")
    if not stem:
        return cands
    ext = "." + ext
    base = re.sub(r"-\d+x\d+$", "", stem)
    cands.append(base + ext)
    base_l = base.lower()
    stem_l = stem.lower()
    for loc, real in LOCAL_IMG.items():
        if loc.startswith(base_l) or loc.startswith(stem_l) or base_l.startswith(re.sub(r"-\d+x\d+$", "", Path(loc).stem)):
            cands.append(real)
    seen = set()
    out = []
    for c in cands:
        k = c.lower()
        if k not in seen:
            seen.add(k)
            out.append(c)
    return out


def resolve_image(basename: str) -> str | None:
    for cand in stem_candidates(basename):
        if cand.lower() in LOCAL_IMG:
            return LOCAL_IMG[cand.lower()]
    return None


def resolve_css(basename: str) -> str | None:
    return LOCAL_CSS.get(basename.lower())


def resolve_js(basename: str) -> str | None:
    return LOCAL_JS.get(basename.lower())


def depth_of(rel_dir: str) -> int:
    if not rel_dir:
        return 0
    return len([p for p in rel_dir.split("/") if p])


def prefix_for(depth: int) -> str:
    return "../" * depth if depth else ""


def rewrite_asset(url: str, prefix: str) -> str | None:
    if not url or url.startswith(("data:", "#", "mailto:", "tel:", "javascript:")):
        return None
    raw = url.strip()
    if raw.startswith("//"):
        raw = "https:" + raw
    # already local
    if raw.startswith(("css/", "js/", "images/", "fonts/", "../")):
        return None

    parsed = urllib.parse.urlparse(raw)
    path = parsed.path or ""
    qs = urllib.parse.parse_qs(parsed.query)

    if "webpc-passthru.php" in path and "src" in qs:
        src = qs["src"][0]
        bn = Path(urllib.parse.unquote(urllib.parse.urlparse(src).path)).name
        local = resolve_image(bn)
        return f"{prefix}images/{local}" if local else None

    if re.search(r"\.(png|jpe?g|gif|svg|webp|ico|avif)(?:$|\?)", path, re.I):
        bn = Path(urllib.parse.unquote(path)).name
        local = resolve_image(bn)
        if local:
            return f"{prefix}images/{local}"
        if "favicon" in bn.lower() and "favicon.png" in LOCAL_IMG:
            return f"{prefix}images/{LOCAL_IMG['favicon.png']}"
        return None

    if path.endswith(".css") or ".css?" in raw:
        bn = Path(path.split("?")[0]).name
        local = resolve_css(bn)
        return f"{prefix}css/{local}" if local else None

    if path.endswith(".js") or ".js?" in raw:
        bn = Path(path.split("?")[0]).name
        local = resolve_js(bn)
        return f"{prefix}js/{local}" if local else None

    if re.search(r"\.(eot|ttf|woff2?|otf)(?:$|\?)", path, re.I):
        bn = Path(path.split("?")[0]).name
        if bn.lower() in LOCAL_FONTS:
            return f"{prefix}fonts/{LOCAL_FONTS[bn.lower()]}"
        return None

    return None


def local_page_href(slug: str, prefix: str, suffix: str) -> str:
    if not slug:
        if not prefix:
            return "/" + suffix if suffix.startswith(("#", "?")) else ("/" if not suffix else "/" + suffix)
        return prefix + "index.html" + suffix
    if not prefix:
        return f"/{slug}/" + suffix
    return f"{prefix}{slug}/index.html" + suffix


def rewrite_href(href: str, prefix: str) -> str:
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return href
    orig = href
    m = re.match(r"^https?://(?:www\.)?recoveris\.io(/.*)?$", href, re.I)
    if m:
        href = m.group(1) or "/"
    elif href.startswith(("http://", "https://")):
        return orig
    if not href.startswith("/"):
        return orig

    path, hash_sep, hash_rest = href.partition("#")
    path_only, qsep, qrest = path.partition("?")
    path_only = path_only.rstrip("/") or "/"
    suffix = (qsep + qrest if qsep else "") + (hash_sep + hash_rest if hash_sep else "")

    if path_only == "/":
        return local_page_href("", prefix, suffix)

    slug = path_only.strip("/")
    first = slug.split("/")[0]
    if first in ALIAS_REDIRECTS and "/" not in slug:
        slug = ALIAS_REDIRECTS[first]

    if slug in SITE_PATHS:
        return local_page_href(slug, prefix, suffix)

    # Category / nested paths already in SITE_PATHS if scraped
    return f"https://recoveris.io/{slug}/" + suffix


def rewrite_srcset(value: str, prefix: str) -> str:
    parts = []
    for chunk in value.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        bits = chunk.split()
        url = bits[0]
        rest = " ".join(bits[1:])
        local = rewrite_asset(url, prefix)
        parts.append(f"{local} {rest}".strip() if local else chunk)
    return ", ".join(parts)


ATTR_RE = re.compile(
    r"""(?P<attr>\b(?:href|src|data-src|data-lazy-src|data-bg|data-background|poster|content))\s*=\s*(?P<q>['"])(?P<url>.*?)(?P=q)""",
    re.I,
)
SRCSET_RE = re.compile(
    r"""(?P<attr>\b(?:srcset|data-srcset|data-lazy-srcset))\s*=\s*(?P<q>['"])(?P<val>.*?)(?P=q)""",
    re.I,
)
CSS_URL_RE = re.compile(r"""url\((?P<q>['"]?)(?P<url>[^'")]+)(?P=q)\)""", re.I)


def process_html(html: str, depth: int) -> tuple[str, dict]:
    prefix = prefix_for(depth)
    stats = {"assets": 0, "links": 0, "unmapped": 0}

    def repl_attr(m: re.Match) -> str:
        attr, q, url = m.group("attr"), m.group("q"), m.group("url")
        low = attr.lower()
        if low == "content":
            if "recoveris.io" in url or "/wp-content/" in url:
                local = rewrite_asset(url, prefix)
                if local:
                    stats["assets"] += 1
                    return f"{attr}={q}{local}{q}"
            return m.group(0)
        if low == "href":
            if any(x in url for x in (".css", ".png", ".svg", ".ico", ".jpg", ".jpeg", ".webp", "webpc-passthru", "/wp-content/", "/wp-includes/")):
                local = rewrite_asset(url, prefix)
                if local:
                    stats["assets"] += 1
                    return f"{attr}={q}{local}{q}"
                if "recoveris.io" in url or url.startswith("/wp-"):
                    stats["unmapped"] += 1
            new = rewrite_href(url, prefix)
            if new != url:
                stats["links"] += 1
                return f"{attr}={q}{new}{q}"
            return m.group(0)
        local = rewrite_asset(url, prefix)
        if local:
            stats["assets"] += 1
            return f"{attr}={q}{local}{q}"
        if "recoveris.io" in url or url.startswith("/wp-"):
            stats["unmapped"] += 1
        return m.group(0)

    def repl_srcset(m: re.Match) -> str:
        val = m.group("val")
        new = rewrite_srcset(val, prefix)
        if new != val:
            stats["assets"] += 1
        return f"{m.group('attr')}={m.group('q')}{new}{m.group('q')}"

    def repl_css(m: re.Match) -> str:
        local = rewrite_asset(m.group("url"), prefix)
        if local:
            stats["assets"] += 1
            return f"url({m.group('q')}{local}{m.group('q')})"
        return m.group(0)

    html = ATTR_RE.sub(repl_attr, html)
    html = SRCSET_RE.sub(repl_srcset, html)
    html = CSS_URL_RE.sub(repl_css, html)
    return html, stats


def slug_file(url_path: str) -> Path:
    """Map URL path to _pages/full/{slug}.html filename used by fetch_full_site."""
    path = url_path.strip("/")
    if not path:
        return FULL / "home.html"
    return FULL / f"{path.replace('/', '__')}.html"


def url_path_from_file(name: str) -> str:
    if name == "home.html":
        return ""
    return name[:-5].replace("__", "/")  # strip .html


def main() -> None:
    global LOCAL_IMG
    LOCAL_IMG = list_local(IMG)  # refresh after downloads

    urls_file = FULL / "_urls.txt"
    urls = [u.strip() for u in urls_file.read_text(encoding="utf-8").splitlines() if u.strip()]

    # Build set of all local paths
    for u in urls:
        p = urllib.parse.urlparse(u).path.strip("/")
        SITE_PATHS.add(p)
    SITE_PATHS.update(ALIAS_REDIRECTS.values())
    SITE_PATHS.update(ALIAS_REDIRECTS.keys())

    print(f"SITE_PATHS={len(SITE_PATHS)} CSS={len(LOCAL_CSS)} JS={len(LOCAL_JS)} IMG={len(LOCAL_IMG)}")

    built = 0
    skipped = 0
    for u in urls:
        path = urllib.parse.urlparse(u).path.strip("/")
        src = slug_file(path)
        if not src.exists() or src.stat().st_size < 500:
            skipped += 1
            print(f"SKIP missing {u}")
            continue

        # Prefer existing localized homepage assets for home
        if not path:
            # Rebuild home from full scrape for link completeness, but keep if we want
            html = src.read_text(encoding="utf-8", errors="replace")
            depth = 0
            html, stats = process_html(html, depth)
            out = MAIN / "index.html"
            out.write_text(html, encoding="utf-8")
        else:
            html = src.read_text(encoding="utf-8", errors="replace")
            depth = depth_of(path)
            html, stats = process_html(html, depth)
            out_dir = MAIN / path
            out_dir.mkdir(parents=True, exist_ok=True)
            out = out_dir / "index.html"
            out.write_text(html, encoding="utf-8")

        built += 1
        if built % 25 == 0 or not path:
            print(f"[{built}] {path or 'home'} assets={stats['assets']} links={stats['links']} unmapped={stats['unmapped']}")

    # Aliases
    for alias, target in ALIAS_REDIRECTS.items():
        out_dir = MAIN / alias
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(
            f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"><meta http-equiv="refresh" content="0;url=/{target}/">
<link rel="canonical" href="/{target}/">
<script>location.replace('/{target}/');</script>
<title>Redirecting…</title></head>
<body><p>Redirecting to <a href="/{target}/">/{target}/</a>…</p></body></html>
""",
            encoding="utf-8",
        )

    print(f"DONE built={built} skipped={skipped}")


if __name__ == "__main__":
    main()
