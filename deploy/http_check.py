import re
import urllib.request

BASE = "http://127.0.0.1:8765"
paths = [
    "/",
    "/solution-for-individuals/",
    "/solution-for-business-vasps/",
    "/digital-asset-recovery/",
    "/blockchain-investigations/",
    "/the-zondacrypto-investigation/",
    "/blog/",
    "/crypto-recovery/",
    "/css/main.11cf34fc32282edf5ca2.css",
    "/images/logo.svg",
]
for path in paths:
    url = BASE + path
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            data = r.read()
        h = ""
        m = re.search(br"<h1[^>]*>(.*?)</h1>", data, re.I | re.S)
        if m:
            h = re.sub(br"<[^>]+>", b" ", m.group(1))
            h = re.sub(br"\s+", b" ", h).strip()[:55].decode("utf-8", "replace")
        print(f"{r.status} {len(data):7d} {path} | {h}")
    except Exception as e:
        print(f"FAIL {path} {e}")

# nested css resolve
html = urllib.request.urlopen(BASE + "/solution-for-individuals/").read().decode("utf-8", "replace")
css = re.findall(r"""href=['"](\.\./css/[^'"]+)""", html)
print("nested css count", len(css))
for c in css[:3]:
    # from /solution-for-individuals/, ../css/x -> /css/x
    u = BASE + "/" + c.replace("../", "")
    code = urllib.request.urlopen(u).status
    print(" ", c, "->", code)
