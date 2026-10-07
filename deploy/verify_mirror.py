#!/usr/bin/env python3
from pathlib import Path
import re

main = Path(r"d:\codes\recoveris.io\main")
pages = [
    "index.html",
    "solution-for-individuals/index.html",
    "solution-for-business-vasps/index.html",
    "digital-asset-recovery/index.html",
    "blockchain-investigations/index.html",
    "blockchain-forensic-training/index.html",
    "blockchain-investigation-management-system/index.html",
    "aftercare-protocol/index.html",
    "source-of-funds-reports/index.html",
    "solution-for-legal-professionals/index.html",
    "solution-for-law-enforcement/index.html",
    "blog/index.html",
    "knowledge-center/index.html",
    "privacy-policy/index.html",
    "terms-and-conditions/index.html",
    "impersonation-recovery-scams-warning/index.html",
]

for p in pages:
    html = (main / p).read_text(encoding="utf-8", errors="replace")
    title = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    t = re.sub(r"<[^>]+>", "", title.group(1)).strip()[:55] if title else "?"
    h = re.sub(r"<[^>]+>", " ", h1.group(1)).strip() if h1 else "?"
    h = re.sub(r"\s+", " ", h)[:55]
    remote_css = len(re.findall(r"href=['\"]https://recoveris\.io[^'\"]+\.css", html))
    local_css = len(re.findall(r"href=['\"](?:\.\./)?css/", html))
    remote_img = len(re.findall(r"src=['\"]https://recoveris\.io", html))
    nav_indiv = "solution-for-individuals" in html
    print(f"{p:55} cssL={local_css:2} cssR={remote_css} imgR={remote_img:3} navOK={nav_indiv} | {h}")

# Sample nested page asset paths
sample = (main / "solution-for-individuals/index.html").read_text(encoding="utf-8", errors="replace")
print("\n--- individuals CSS sample ---")
for m in re.finditer(r'href=[\'"]([^\'"]+\.css)', sample):
    print(" ", m.group(1))
    if m.start() > 5000:
        break

print("\n--- individuals nav sample ---")
for m in re.finditer(r'class="header-link"[^>]*href=[\'"]([^\'"]+)', sample):
    print(" ", m.group(1))

# Unmapped blog images
blog = (main / "blog/index.html").read_text(encoding="utf-8", errors="replace")
remote = sorted(set(re.findall(r"https://recoveris\.io[^\"'\s>]+", blog)))
print(f"\nblog remote URLs: {len(remote)}")
for u in remote[:20]:
    print(" ", u[:120])
