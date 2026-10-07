import re
import pathlib

root = pathlib.Path(r"d:\codes\recoveris.io\_pages")
for f in sorted(root.glob("*.html")):
    html = f.read_text(encoding="utf-8", errors="replace")
    classes = re.findall(r"<section[^>]*class=\"([^\"]+)\"", html)
    print(f"{f.stem}:")
    for c in classes:
        print(f"  - {c}")
    print()
