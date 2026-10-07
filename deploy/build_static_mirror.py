#!/usr/bin/env python3
"""Build a full static mirror of recoveris.io under main/ from _pages/ HTML."""
from __future__ import annotations

import re
import urllib.parse
from pathlib import Path

ROOT = Path(r"d:\codes\recoveris.io")
PAGES_DIR = ROOT / "_pages"
MAIN_DIR = ROOT / "main"
IMG_DIR = MAIN_DIR / "images"
CSS_DIR = MAIN_DIR / "css"
JS_DIR = MAIN_DIR / "js"

# slug key in _pages -> URL path under main (directory with index.html)
PAGE_MAP = {
    "home": "",
    "individuals": "solution-for-individuals",
    "business": "solution-for-business-vasps",
    "legal": "solution-for-legal-professionals",
    "law-enforcement": "solution-for-law-enforcement",
    "investigations": "blockchain-investigations",
    "recovery": "digital-asset-recovery",
    "source-of-funds": "source-of-funds-reports",
    "aftercare": "aftercare-protocol",
    "training": "blockchain-forensic-training",
    "bims": "blockchain-investigation-management-system",
    "terms": "terms-and-conditions",
    "privacy": "privacy-policy",
    "scam-warning": "impersonation-recovery-scams-warning",
    "blog": "blog",
    "knowledge-center": "knowledge-center",
}

# Alternate permalinks seen in homepage links that should resolve locally
ALIAS_REDIRECTS = {
    "asset-recovery": "digital-asset-recovery",
    "investigations": "blockchain-investigations",
    "intelligence": "blockchain-investigation-management-system",
}

# Known basename remaps when saveweb2zip used a different filename
BASENAME_ALIASES = {
    "IMG_3877-scaled.png": "IMG_3877-768x1024.png",
    "Prinz-scaled.jpeg": "Prinz-768x1024.jpeg",
    "1inch-logo-2.png": "1inch-logo-2.png",
}


def list_local(folder: Path) -> dict[str, str]:
    """Map lowercase basename -> actual filename."""
    out: dict[str, str] = {}
    if not folder.exists():
        return out
    for p in folder.iterdir():
        if p.is_file():
            out[p.name.lower()] = p.name
    return out


LOCAL_CSS = list_local(CSS_DIR)
LOCAL_JS = list_local(JS_DIR)
LOCAL_IMG = list_local(IMG_DIR)


def stem_variants(name: str) -> list[str]:
    """Generate candidate local filenames for an upload basename."""
    name = urllib.parse.unquote(name)
    candidates = [name]
    if name in BASENAME_ALIASES:
        candidates.append(BASENAME_ALIASES[name])

    # strip -scaled
    if "-scaled." in name:
        candidates.append(name.replace("-scaled.", "."))

    stem, _, ext = name.rpartition(".")
    if not stem:
        return candidates
    ext = "." + ext

    # WordPress size suffixes: -1024x768, -300x44, etc.
    m = re.match(r"^(.*?)(?:-\d+x\d+)?$", stem)
    base = m.group(1) if m else stem
    candidates.append(base + ext)

    # Prefer any local file that starts with base
    base_l = base.lower()
    for loc in LOCAL_IMG:
        if loc.startswith(base_l) or loc.startswith(stem.lower()):
            candidates.append(LOCAL_IMG[loc])

    # Also try common resized names present locally
    for loc_name in LOCAL_IMG.values():
        loc_stem = Path(loc_name).stem.lower()
        if loc_stem.startswith(base_l) or base_l.startswith(re.sub(r"-\d+x\d+$", "", loc_stem)):
            candidates.append(loc_name)

    # de-dupe preserve order
    seen = set()
    uniq = []
    for c in candidates:
        k = c.lower()
        if k not in seen:
            seen.add(k)
            uniq.append(c)
    return uniq


def resolve_image(basename: str) -> str | None:
    for cand in stem_variants(basename):
        key = cand.lower()
        if key in LOCAL_IMG:
            return LOCAL_IMG[key]
    return None


def resolve_css(basename: str) -> str | None:
    key = basename.lower()
    if key in LOCAL_CSS:
        return LOCAL_CSS[key]
    # main theme style.css vs styles.css
    if key == "style.css" and "style.css" in LOCAL_CSS:
        return LOCAL_CSS["style.css"]
    return None


def resolve_js(basename: str) -> str | None:
    key = basename.lower()
    if key in LOCAL_JS:
        return LOCAL_JS[key]
    return None


def asset_prefix(depth: int) -> str:
    if depth <= 0:
        return ""
    return "../" * depth


def rewrite_url_to_local(url: str, prefix: str) -> str | None:
    """Return local relative URL if we can map it, else None (leave as-is)."""
    if not url or url.startswith("data:") or url.startswith("#") or url.startswith("mailto:"):
        return None

    # Normalize
    raw = url.strip()
    # protocol-relative
    if raw.startswith("//"):
        raw = "https:" + raw

    parsed = urllib.parse.urlparse(raw)
    path = parsed.path or ""
    query = urllib.parse.parse_qs(parsed.query)

    # webpc-passthru.php?src=...
    if "webpc-passthru.php" in path and "src" in query:
        src = query["src"][0]
        src_path = urllib.parse.urlparse(src).path
        basename = Path(urllib.parse.unquote(src_path)).name
        local = resolve_image(basename)
        if local:
            return f"{prefix}images/{local}"
        return None

    # Direct uploads / theme / plugin media
    if re.search(r"\.(png|jpe?g|gif|svg|webp|ico|avif)(?:$|\?)", path, re.I):
        basename = Path(urllib.parse.unquote(path)).name
        # fonts under css? dashicons
        if path.endswith((".eot", ".ttf", ".woff", ".woff2")):
            # keep remote or map if we have fonts/
            font = MAIN_DIR / "fonts" / basename
            if font.exists():
                return f"{prefix}fonts/{basename}"
            return None
        local = resolve_image(basename)
        if local:
            return f"{prefix}images/{local}"
        # favicon sometimes in theme
        if "favicon" in basename.lower():
            if "favicon.png" in LOCAL_IMG:
                return f"{prefix}images/{LOCAL_IMG['favicon.png']}"
        return None

    if path.endswith(".css") or ".css?" in raw:
        basename = Path(path.split("?")[0]).name
        local = resolve_css(basename)
        if local:
            return f"{prefix}css/{local}"
        return None

    if path.endswith(".js") or ".js?" in raw:
        basename = Path(path.split("?")[0]).name
        local = resolve_js(basename)
        if local:
            return f"{prefix}js/{local}"
        return None

    if re.search(r"\.(eot|ttf|woff2?|otf)(?:$|\?)", path, re.I):
        basename = Path(path.split("?")[0]).name
        font = MAIN_DIR / "fonts" / basename
        if font.exists():
            return f"{prefix}fonts/{basename}"
        return None

    return None


def rewrite_internal_href(href: str, prefix: str) -> str:
    """Map recoveris.io absolute and root-relative page links to local paths."""
    if not href:
        return href

    if href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return href

    orig = href
    was_absolute_recoveris = False
    m = re.match(r"^https?://(?:www\.)?recoveris\.io(/.*)?$", href, re.I)
    if m:
        was_absolute_recoveris = True
        href = m.group(1) or "/"
    elif href.startswith("https://") or href.startswith("http://"):
        return orig

    if not href.startswith("/"):
        return orig

    path, hash_sep, hash_rest = href.partition("#")
    path_only, qsep, qrest = path.partition("?")
    path_only = path_only.rstrip("/") or "/"
    suffix = (qsep + qrest if qsep else "") + (hash_sep + hash_rest if hash_sep else "")

    def home_href() -> str:
        if not prefix:
            return "/" + suffix.lstrip("/") if suffix.startswith("#") else ("/" + suffix if suffix else "/")
        # nested -> ../index.html#about
        return prefix + "index.html" + suffix

    if path_only == "/":
        if not prefix:
            if suffix.startswith("#"):
                return "/" + suffix
            if suffix.startswith("?"):
                return "/" + suffix
            return "/"
        return home_href()

    slug = path_only.strip("/")
    first = slug.split("/")[0]
    if first in ALIAS_REDIRECTS and "/" not in slug:
        slug = ALIAS_REDIRECTS[first]

    known = set(PAGE_MAP.values()) - {""}

    if slug in known:
        if not prefix:
            return f"/{slug}/" + suffix
        return f"{prefix}{slug}/index.html" + suffix

    if slug == "blog":
        if not prefix:
            return "/blog/" + suffix
        return f"{prefix}blog/index.html" + suffix

    if slug.startswith("blog/"):
        # Individual posts not mirrored — keep pointing at live site
        return f"https://recoveris.io/{slug}/" + suffix

    # Unmapped site paths: keep absolute recoveris URL so nothing 404s silently
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
        local = rewrite_url_to_local(url, prefix)
        if local:
            parts.append(f"{local} {rest}".strip())
        else:
            parts.append(chunk)
    return ", ".join(parts)


ATTR_URL_RE = re.compile(
    r"""(?P<attr>\b(?:href|src|data-src|data-lazy-src|data-bg|data-background|poster|content))\s*=\s*(?P<q>['"])(?P<url>.*?)(?P=q)""",
    re.I,
)
SRCSET_RE = re.compile(
    r"""(?P<attr>\b(?:srcset|data-srcset|data-lazy-srcset))\s*=\s*(?P<q>['"])(?P<val>.*?)(?P=q)""",
    re.I,
)
CSS_URL_RE = re.compile(r"""url\((?P<q>['"]?)(?P<url>[^'")]+)(?P=q)\)""", re.I)


def process_html(html: str, depth: int) -> tuple[str, dict]:
    prefix = asset_prefix(depth)
    stats = {"assets": 0, "links": 0, "unmapped_assets": 0}

    def repl_attr(m: re.Match) -> str:
        attr = m.group("attr")
        q = m.group("q")
        url = m.group("url")

        # og:image and similar content= that are images
        if attr.lower() == "content":
            if "recoveris.io" in url or url.startswith("/wp-content"):
                local = rewrite_url_to_local(url, prefix)
                if local:
                    stats["assets"] += 1
                    return f"{attr}={q}{local}{q}"
            return m.group(0)

        if attr.lower() == "href":
            # stylesheet or icon?
            if any(x in url for x in (".css", ".png", ".svg", ".ico", ".jpg", "webpc-passthru", "/wp-content/", "/wp-includes/")):
                local = rewrite_url_to_local(url, prefix)
                if local:
                    stats["assets"] += 1
                    return f"{attr}={q}{local}{q}"
                if "recoveris.io" in url or url.startswith("/wp-"):
                    stats["unmapped_assets"] += 1
                # page link
            new_href = rewrite_internal_href(url, prefix)
            if new_href != url:
                stats["links"] += 1
                return f"{attr}={q}{new_href}{q}"
            return m.group(0)

        # src / data-src / etc
        local = rewrite_url_to_local(url, prefix)
        if local:
            stats["assets"] += 1
            return f"{attr}={q}{local}{q}"
        if "recoveris.io" in url or url.startswith("/wp-"):
            stats["unmapped_assets"] += 1
        return m.group(0)

    def repl_srcset(m: re.Match) -> str:
        attr = m.group("attr")
        q = m.group("q")
        val = m.group("val")
        new_val = rewrite_srcset(val, prefix)
        if new_val != val:
            stats["assets"] += 1
        return f"{attr}={q}{new_val}{q}"

    html = ATTR_URL_RE.sub(repl_attr, html)
    html = SRCSET_RE.sub(repl_srcset, html)

    # Inline style url(...)
    def repl_css_url(m: re.Match) -> str:
        url = m.group("url")
        local = rewrite_url_to_local(url, prefix)
        if local:
            stats["assets"] += 1
            return f"url({m.group('q')}{local}{m.group('q')})"
        return m.group(0)

    html = CSS_URL_RE.sub(repl_css_url, html)

    # Fix root-relative asset refs that may remain: /wp-content/...
    def repl_root_asset(m: re.Match) -> str:
        full = m.group(0)
        url = m.group(1)
        local = rewrite_url_to_local("https://recoveris.io" + url, prefix)
        if local:
            stats["assets"] += 1
            return full.replace(url, local)
        return full

    html = re.sub(
        r"""((?:href|src|data-src)=['"])(/wp-(?:content|includes)/[^'"]+)""",
        lambda m: (
            f"{m.group(1)}{rewrite_url_to_local('https://recoveris.io' + m.group(2), prefix) or m.group(2)}"
        ),
        html,
        flags=re.I,
    )

    return html, stats


def write_page(key: str, rel_dir: str) -> None:
    src = PAGES_DIR / f"{key}.html"
    if not src.exists():
        print(f"SKIP missing {src}")
        return

    if rel_dir == "":
        # Prefer already-localized main/index.html if present and fresher workflow:
        # Still rebuild from _pages for consistency of link rewriting, OR keep main/index
        # and only rewrite remaining absolute page links.
        out_path = MAIN_DIR / "index.html"
        depth = 0
        # If main/index already localized assets, rewrite links only on it
        html = out_path.read_text(encoding="utf-8", errors="replace")
        html, stats = process_html(html, depth)
        out_path.write_text(html, encoding="utf-8")
        print(f"OK home -> {out_path.relative_to(ROOT)} assets={stats['assets']} links={stats['links']} unmapped={stats['unmapped_assets']}")
        return

    html = src.read_text(encoding="utf-8", errors="replace")
    depth = 1
    html, stats = process_html(html, depth)

    out_dir = MAIN_DIR / rel_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    out_path.write_text(html, encoding="utf-8")
    print(
        f"OK {key:20} -> {out_path.relative_to(ROOT)} "
        f"assets={stats['assets']} links={stats['links']} unmapped={stats['unmapped_assets']}"
    )


def write_alias_stubs() -> None:
    """Create alias directories that redirect via meta refresh to canonical pages."""
    for alias, target in ALIAS_REDIRECTS.items():
        out_dir = MAIN_DIR / alias
        out_dir.mkdir(parents=True, exist_ok=True)
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url=../{target}/">
  <link rel="canonical" href="/{target}/">
  <title>Redirecting…</title>
  <script>location.replace("../{target}/");</script>
</head>
<body>
  <p>Redirecting to <a href="../{target}/">/{target}/</a>…</p>
</body>
</html>
"""
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        print(f"OK alias {alias} -> {target}")


def main() -> None:
    print(f"CSS={len(LOCAL_CSS)} JS={len(LOCAL_JS)} IMG={len(LOCAL_IMG)}")
    for key, rel in PAGE_MAP.items():
        write_page(key, rel)
    write_alias_stubs()
    print("DONE")


if __name__ == "__main__":
    main()
