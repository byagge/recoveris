#!/usr/bin/env python3
import ssl
import time
import urllib.request

ctx = ssl.create_default_context()


def fetch(url, encoding="gzip, deflate"):
    t = time.time()
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept-Encoding": encoding,
            "Accept-Language": "ru",
        },
    )
    with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
        raw = r.read()
        headers = dict(r.headers)
    return time.time() - t, raw, headers


for enc in ("identity", "gzip, deflate"):
    dt, raw, h = fetch("https://recoveris.arix.vu/", enc)
    print(
        f"home enc_req={enc!r} time={dt:.2f}s bytes={len(raw)} "
        f"ce={h.get('Content-Encoding','-')} vary={h.get('Vary','-')}"
    )

dt, raw, h = fetch("https://recoveris.arix.vu/")
text = raw.decode("utf-8", "replace")
checks = [
    "Главная",
    "ВЕРНУТЬ СРЕДСТВА",
    "Кому помогаем",
    "Агентные расследования",
    "Нам доверяют",
    "Для частных лиц",
    "manrope.css",
    "fonts.googleapis",
]
for c in checks:
    print(f"  {c!r}: {c in text}")

dt2, raw2, _ = fetch("https://recoveris.arix.vu/solution-for-individuals/")
t2 = raw2.decode("utf-8", "replace")
print("individuals H1 RU?", "Для частных лиц" in t2)
print(f"individuals time={dt2:.2f}s bytes={len(raw2)}")
