#!/usr/bin/env python3
"""Resume downloading missing images referenced by _pages/full HTML."""
from __future__ import annotations

import re
import ssl
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(r"d:\codes\recoveris.io")
FULL = ROOT / "_pages" / "full"
IMG_DIR = ROOT / "main" / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = {"User-Agent": "Mozilla/5.0 (compatible; RecoverisMirror/1.0)"}


def fetch(url: str) -> bytes:
    # Ensure path is properly percent-encoded
    parts = urllib.parse.urlsplit(url)
    path = urllib.parse.quote(urllib.parse.unquote(parts.path), safe="/:@")
    encoded = urllib.parse.urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))
    req = urllib.request.Request(encoded, headers=UA)
    with urllib.request.urlopen(req, context=ctx, timeout=90) as r:
        return r.read()


def safe_name(bn: str) -> str:
    # Windows-safe filename
    bn = bn.replace("\u0301", "").replace(":", "_").replace("?", "_").replace("*", "_")
    return bn


def main() -> None:
    url_by_bn: dict[str, str] = {}
    for html_path in FULL.glob("*.html"):
        html = html_path.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(
            r"(https://recoveris\.io/wp-content/uploads/[^\s\"'<>]+\.(?:png|jpe?g|gif|svg|webp))",
            html,
            re.I,
        ):
            u = m.group(1).split("&")[0].split("?")[0]
            bn = Path(urllib.parse.unquote(urllib.parse.urlparse(u).path)).name
            url_by_bn.setdefault(bn, u)
        for m in re.finditer(
            r"webpc-passthru\.php\?src=(https://recoveris\.io/wp-content/uploads/[^&\"']+)",
            html,
        ):
            u = urllib.parse.unquote(m.group(1)).split("?")[0]
            bn = Path(urllib.parse.urlparse(u).path).name
            url_by_bn.setdefault(bn, u)

    local = {p.name.lower() for p in IMG_DIR.iterdir() if p.is_file()}
    downloaded = 0
    skipped = 0
    failed = 0
    for bn, url in sorted(url_by_bn.items()):
        dest_name = safe_name(bn)
        if dest_name.lower() in local or bn.lower() in local:
            skipped += 1
            continue
        # also skip if a resized variant exists for same base
        base = re.sub(r"-\d+x\d+$", "", Path(bn).stem).lower()
        if any(x.startswith(base) and Path(x).suffix.lower() == Path(bn).suffix.lower() for x in local):
            # still download exact if it's a featured size we don't have — prefer exact
            pass
        dest = IMG_DIR / dest_name
        try:
            data = fetch(url)
            dest.write_bytes(data)
            local.add(dest_name.lower())
            downloaded += 1
            if downloaded % 10 == 0:
                print(f"downloaded {downloaded}...")
            time.sleep(0.05)
        except Exception as e:
            failed += 1
            print(f"FAIL {dest_name.encode('ascii','replace').decode()}: {e}")

    print(f"done downloaded={downloaded} skipped={skipped} failed={failed} total_refs={len(url_by_bn)}")


if __name__ == "__main__":
    main()
