#!/usr/bin/env python3
"""Fetch all recoveris.io URLs from sitemaps into _pages/full/ and download missing images."""
from __future__ import annotations

import re
import ssl
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(r"d:\codes\recoveris.io")
OUT = ROOT / "_pages" / "full"
IMG_DIR = ROOT / "main" / "images"
OUT.mkdir(parents=True, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = {"User-Agent": "Mozilla/5.0 (compatible; RecoverisMirror/1.0)"}


def fetch(url: str, timeout: int = 90) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, context=ctx, timeout=timeout) as r:
        return r.read()


def sitemap_locs(xml: str) -> list[str]:
    return re.findall(r"<loc>\s*([^<]+)\s*</loc>", xml)


def slug_from_url(url: str) -> str:
    path = urllib.parse.urlparse(url).path.strip("/")
    if not path:
        return "home"
    return path.replace("/", "__")


def main() -> None:
    index = fetch("https://recoveris.io/sitemap_index.xml").decode("utf-8", "replace")
    maps = sitemap_locs(index)
    print("sitemaps:", maps)

    urls: list[str] = []
    for sm in maps:
        xml = fetch(sm).decode("utf-8", "replace")
        locs = sitemap_locs(xml)
        print(f"  {sm}: {len(locs)} urls")
        urls.extend(locs)

    # unique preserve order
    seen = set()
    uniq = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            uniq.append(u)
    print(f"total unique URLs: {len(uniq)}")

    # Save URL list
    (OUT / "_urls.txt").write_text("\n".join(uniq), encoding="utf-8")

    missing_imgs: set[str] = set()
    ok = 0
    fail = 0
    for i, url in enumerate(uniq, 1):
        slug = slug_from_url(url)
        path = OUT / f"{slug}.html"
        if path.exists() and path.stat().st_size > 1000:
            html = path.read_text(encoding="utf-8", errors="replace")
        else:
            try:
                raw = fetch(url)
                html = raw.decode("utf-8", "replace")
                path.write_text(html, encoding="utf-8")
                ok += 1
                print(f"[{i}/{len(uniq)}] OK {url}")
                time.sleep(0.15)
            except Exception as e:
                fail += 1
                print(f"[{i}/{len(uniq)}] FAIL {url}: {e}")
                continue

        # Collect image basenames
        for m in re.finditer(
            r"webpc-passthru\.php\?src=https://recoveris\.io/wp-content/uploads/[^&\"']+/([^&\"'?]+)",
            html,
        ):
            missing_imgs.add(urllib.parse.unquote(m.group(1)))
        for m in re.finditer(
            r"https://recoveris\.io/wp-content/uploads/[^\"']+/([^\"'/?]+\.(?:png|jpe?g|gif|svg|webp))",
            html,
            re.I,
        ):
            missing_imgs.add(urllib.parse.unquote(m.group(1)))

    print(f"fetched new={ok} fail={fail}")

    # Download missing images
    local = {p.name.lower() for p in IMG_DIR.iterdir() if p.is_file()} if IMG_DIR.exists() else set()
    to_get = []
    for bn in sorted(missing_imgs):
        stem = Path(bn).stem
        # skip if any local starts with stem base
        base = re.sub(r"-\d+x\d+$", "", stem).lower()
        if bn.lower() in local:
            continue
        if any(x.startswith(base) for x in local):
            continue
        to_get.append(bn)

    print(f"candidate missing images: {len(to_get)}")

    # Find full upload URLs from saved HTML to download
    url_by_bn: dict[str, str] = {}
    for html_path in OUT.glob("*.html"):
        html = html_path.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(
            r"(https://recoveris\.io/wp-content/uploads/[^\s\"'<>]+\.(?:png|jpe?g|gif|svg|webp))",
            html,
            re.I,
        ):
            u = m.group(1).split("?")[0]
            bn = Path(urllib.parse.unquote(urllib.parse.urlparse(u).path)).name
            url_by_bn.setdefault(bn, u)
        for m in re.finditer(
            r"webpc-passthru\.php\?src=(https://recoveris\.io/wp-content/uploads/[^&\"']+)",
            html,
        ):
            u = urllib.parse.unquote(m.group(1)).split("?")[0]
            bn = Path(urllib.parse.urlparse(u).path).name
            url_by_bn.setdefault(bn, u)

    downloaded = 0
    for bn in to_get:
        if bn not in url_by_bn:
            continue
        dest = IMG_DIR / bn
        if dest.exists():
            continue
        try:
            data = fetch(url_by_bn[bn])
            dest.write_bytes(data)
            downloaded += 1
            print(f"  IMG {bn} ({len(data)} bytes)")
            time.sleep(0.05)
        except Exception as e:
            print(f"  IMG FAIL {bn}: {e}")

    print(f"downloaded images: {downloaded}")
    print("DONE")


if __name__ == "__main__":
    main()
