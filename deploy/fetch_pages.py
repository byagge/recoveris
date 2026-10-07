"""Download recoveris.io pages HTML to D: for content extraction."""
import os
import re
import ssl
import urllib.request
from html import unescape
from pathlib import Path

OUT = Path(r"d:\codes\recoveris.io\_pages")
OUT.mkdir(exist_ok=True)

PAGES = {
    "home": "https://recoveris.io/",
    "individuals": "https://recoveris.io/solution-for-individuals/",
    "business": "https://recoveris.io/solution-for-business-vasps/",
    "legal": "https://recoveris.io/solution-for-legal-professionals/",
    "law-enforcement": "https://recoveris.io/solution-for-law-enforcement/",
    "investigations": "https://recoveris.io/blockchain-investigations/",
    "recovery": "https://recoveris.io/digital-asset-recovery/",
    "source-of-funds": "https://recoveris.io/source-of-funds-reports/",
    "aftercare": "https://recoveris.io/aftercare-protocol/",
    "training": "https://recoveris.io/blockchain-forensic-training/",
    "bims": "https://recoveris.io/blockchain-investigation-management-system/",
    "terms": "https://recoveris.io/terms-and-conditions/",
    "privacy": "https://recoveris.io/privacy-policy/",
    "scam-warning": "https://recoveris.io/impersonation-recovery-scams-warning/",
    "blog": "https://recoveris.io/blog/",
    "knowledge-center": "https://recoveris.io/knowledge-center/",
}

ctx = ssl.create_default_context()
# some hosts need looser SSL in this env
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

UA = {"User-Agent": "Mozilla/5.0 (compatible; RecoverisMirror/1.0)"}


def strip_tags(html: str) -> str:
    html = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", html)
    html = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", html)
    html = re.sub(r"(?is)<!--.*?-->", " ", html)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    html = re.sub(r"</p>|</h[1-6]>|</li>|</div>", "\n", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    html = unescape(html)
    html = re.sub(r"[ \t]+", " ", html)
    html = re.sub(r"\n\s*\n+", "\n\n", html)
    return html.strip()


def extract(html: str) -> dict:
    title = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    # main content region if present
    main = re.search(r"(?is)<main[^>]*>(.*?)</main>", html)
    body = main.group(1) if main else html
    headings = [
        re.sub(r"<[^>]+>", "", unescape(m.group(1))).strip()
        for m in re.finditer(r"<h([1-3])[^>]*>(.*?)</h\1>", body, re.I | re.S)
    ]
    # paragraphs
    paras = []
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", body, re.I | re.S):
        t = re.sub(r"<[^>]+>", "", unescape(m.group(1))).strip()
        t = re.sub(r"\s+", " ", t)
        if len(t) > 40:
            paras.append(t)
    return {
        "title": unescape(title.group(1)).strip() if title else "",
        "h1": re.sub(r"<[^>]+>", "", unescape(h1.group(1))).strip() if h1 else "",
        "headings": headings[:40],
        "paragraphs": paras[:60],
        "text": strip_tags(body)[:12000],
    }


for key, url in PAGES.items():
    path = OUT / f"{key}.html"
    meta_path = OUT / f"{key}.txt"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
            raw = r.read()
        # try utf-8
        html = raw.decode("utf-8", errors="replace")
        path.write_text(html, encoding="utf-8")
        info = extract(html)
        lines = [
            f"URL: {url}",
            f"TITLE: {info['title']}",
            f"H1: {info['h1']}",
            "",
            "HEADINGS:",
            *[f"- {h}" for h in info["headings"]],
            "",
            "PARAGRAPHS:",
            *[f"- {p}" for p in info["paragraphs"]],
            "",
            "TEXT:",
            info["text"],
        ]
        meta_path.write_text("\n".join(lines), encoding="utf-8")
        print("OK", key, len(html))
    except Exception as e:
        print("FAIL", key, e)

print("DONE", OUT)
