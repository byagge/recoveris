from pathlib import Path
import re

main = Path(r"d:\codes\recoveris.io\main")
pages = list(main.rglob("index.html"))
print("pages", len(pages))
checks = [
    "",
    "solution-for-individuals",
    "solution-for-business-vasps",
    "digital-asset-recovery",
    "the-zondacrypto-investigation",
    "blog",
    "blockchain-forensic-training",
    "privacy-policy",
    "crypto-recovery",
    "odzyskiwanie-kryptowalut",
]
for c in checks:
    p = main / "index.html" if not c else main / c / "index.html"
    html = p.read_text(encoding="utf-8", errors="replace")
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    h = re.sub(r"<[^>]+>", " ", h1.group(1) if h1 else "?")
    h = re.sub(r"\s+", " ", h).strip()[:60]
    css = len(re.findall(r"""href=['"](?:\.\./)*css/""", html))
    rem = len(re.findall(r"""href=['"]https://recoveris\.io[^'"]*\.css""", html))
    print(f"{(c or 'home'):40} cssL={css} cssR={rem} | {h}")
print("images", len(list((main / "images").iterdir())))

# Verify individuals body section uniqueness vs business
a = (main / "solution-for-individuals/index.html").read_text(encoding="utf-8", errors="replace")
b = (main / "solution-for-business-vasps/index.html").read_text(encoding="utf-8", errors="replace")
print("individuals==business?", a == b)
print("individuals len", len(a), "business len", len(b))
