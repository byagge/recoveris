#!/usr/bin/env python3
import re
import time
from pathlib import Path

import translators as ts

MAIN = Path(r"d:\codes\recoveris.io\main")
PAGES = [
    "index.html",
    "solution-for-individuals/index.html",
    "solution-for-business-vasps/index.html",
    "solution-for-legal-professionals/index.html",
    "solution-for-law-enforcement/index.html",
    "digital-asset-recovery/index.html",
    "blockchain-investigations/index.html",
    "blockchain-forensic-training/index.html",
    "blockchain-investigation-management-system/index.html",
    "source-of-funds-reports/index.html",
    "aftercare-protocol/index.html",
    "blog/index.html",
    "knowledge-center/index.html",
    "privacy-policy/index.html",
    "terms-and-conditions/index.html",
    "impersonation-recovery-scams-warning/index.html",
    "newsletter/index.html",
    "services/index.html",
]

NAME_RE = re.compile(r"^[A-Z][a-z]+(?:\s+[A-Z][a-z'\-]+){0,3}$")


def main() -> None:
    seen: set[str] = set()
    strings: list[str] = []
    for rel in PAGES:
        html = (MAIN / rel).read_text(encoding="utf-8")
        for m in re.finditer(r"<(p|h1|h2|h3|h4|li)[^>]*>([^<]{20,600})</\1>", html, re.I):
            t = m.group(2).strip()
            if not re.search(r"[A-Za-z]{5,}", t):
                continue
            if re.search(r"[А-Яа-яЁё]", t):
                continue
            if NAME_RE.fullmatch(t):
                continue
            if t not in seen:
                seen.add(t)
                strings.append(t)

    print(f"leftover={len(strings)}", flush=True)
    mapping: dict[str, str] = {}
    for i, s in enumerate(strings, 1):
        clean = (
            s.replace("&#8217;", "'")
            .replace("&#8216;", "'")
            .replace("&#038;", "&")
            .replace("&amp;", "&")
            .replace("&nbsp;", " ")
        )
        try:
            ru = ts.translate_text(
                clean[:4500],
                translator="bing",
                from_language="en",
                to_language="ru",
            )
            mapping[s] = ru
            print(f"[{i}/{len(strings)}] ok", flush=True)
            time.sleep(0.12)
        except Exception as e:
            print(f"[{i}] fail {e}", flush=True)
            mapping[s] = s

    # structural fixes
    mapping["For Частные лица"] = "Для частных лиц"
    mapping["For Бизнес и VASP"] = "Для бизнеса и VASP"
    mapping["For Юристы"] = "Для юристов"
    mapping["For Правоохранение"] = "Для правоохранения"

    changed = 0
    for p in MAIN.rglob("index.html"):
        html = p.read_text(encoding="utf-8")
        new = html
        for a, b in sorted(mapping.items(), key=lambda x: -len(x[0])):
            if a != b:
                new = new.replace(a, b)
        if new != html:
            p.write_text(new, encoding="utf-8")
            changed += 1
    print(f"DONE changed={changed}", flush=True)


if __name__ == "__main__":
    main()
