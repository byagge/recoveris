#!/usr/bin/env python3
"""Translate English content on EN pages in main/ to Russian."""
from __future__ import annotations

import json
import re
import time
from html.parser import HTMLParser
from pathlib import Path

import translators as ts

ROOT = Path(r"d:\codes\recoveris.io")
MAIN = ROOT / "main"
CACHE = ROOT / "_pages" / "translate_cache_bing.json"
CACHE.parent.mkdir(parents=True, exist_ok=True)

# Non-English SEO landings — leave alone
SKIP_PREFIXES = (
    "odzyskiwanie-",
    "zhuihui-",
    "recuperar-",
    "recuperare-",
    "recuperer-",
    "cryptovaluta-",
    "kryptowaehrungen-",
    "vernut-",
    "amhohwapye-",
    "angoshisan-",
    "istirdad-",
    "kripto-",
    "krypto-",
    "aterfa-",
    "genvinde-",
    "gjenopprette-",
    "varastetun-",
    "hjaelp-",
    "tasayyud-",
    "jiamihuobi-",
    "phishing-cripto",
    "phishing-crypto",
    "phishing-krypto",
    "estafa-",
    "calinan-",
    "mahfazat-",
    "tether-dongjie",
    "billetera-",
    "portefeuille-",
    "wallet-usdt-congelato",
    "usdt-wallet-von-",
    "portfel-usdt-",
    "jak-",
    "sledztwo-",
)

KEEP = {
    "Aftercare Protocol",
    "Recoveris",
    "BIMS",
    "Source of Funds",
    "LinkedIn",
    "YouTube",
    "Twitter",
    "FAQ",
    "CEO",
    "CTO",
    "CFO",
    "EY",
    "1inch",
    "Upbit",
    "Tornado Cash",
    "ZondaCrypto",
    "Zondacrypto",
    "OSCE",
    "Interpol",
    "Europol",
    "FBI",
}

NAME_RE = re.compile(
    r"^[A-ZÀ-ÖØ-Þ][a-zà-öø-ÿ''\-]+(?:\s+[A-ZÀ-ÖØ-Þ][a-zà-öø-ÿ''\-]+){0,3}$"
)

FIXED = {
    "read more": "читать далее",
    "Read more": "Читать далее",
    "Learn more": "Подробнее",
    "Legal professionals": "Юристы",
    "Don't see your exact situation?": "Не видите свою ситуацию?",
    "Swiss-based, globally connected": "Швейцарская база, глобальные связи",
    "A team you can verify": "Команда, которую можно проверить",
    "Heritage in law enforcement": "Опыт правоохранения",
    "1. Initial Case Assessment": "1. Первичная оценка дела",
    "2. Strategic Recovery Plan": "2. Стратегический план возврата",
    "3. Execution & Enforcement": "3. Исполнение и принуждение",
    "1. Romance Scam": "1. Романтический скам",
    "2. The Impersonation Scam": "2. Скам с имперсонацией",
    "3. Investment Scam": "3. Инвестиционный скам",
    "4. Fake Exchange or Investing Platform": "4. Фейковая биржа или инвестплатформа",
    "5. Malicious Link or Wallet Drainer": "5. Вредоносная ссылка или wallet drainer",
    "6. Hack or Malware": "6. Взлом или вредоносное ПО",
    "7. Physical Theft or Coerced Transfer": "7. Физическая кража или принуждение к переводу",
    "BIMS: Your Investigative Operating System": "BIMS: ваша операционная система расследований",
    "Cross-Chain Correlation": "Кросс-чейн корреляция",
    "Privacy Protocol & Mixer Analysis": "Анализ privacy-протоколов и миксеров",
    "Legal-Grade Reporting & Auditability": "Юридически значимая отчётность и аудитируемость",
    "EY announcement:": "Анонс EY:",
    "INTELLIGENCE": "РАЗВЕДКА",
    "OPERATIONS": "ОПЕРАЦИИ",
    "PRODUCT": "ПРОДУКТ",
    "Connect with our team": "Связаться с нашей командой",
    "Our recovery framework": "Наш фреймворк возврата",
    "Who we serve": "Кого мы обслуживаем",
    "Our videos": "Наши видео",
    "The Recoveris team": "Команда Recoveris",
    "Case studies": "Кейсы",
    "Our recent posts": "Недавние публикации",
    "Begin Your Recovery": "Начните возврат средств",
    "Member of elite associations": "Участник ведущих ассоциаций",
    "Associations": "Ассоциации",
    "Recoveris in media": "Recoveris в СМИ",
}


class TextCollector(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "path", "code", "pre"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.texts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.SKIP:
            self._skip += 1

    def handle_endtag(self, tag):
        if tag.lower() in self.SKIP and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self._skip:
            return
        t = re.sub(r"\s+", " ", data).strip()
        if t:
            self.texts.append(t)


def load_cache() -> dict[str, str]:
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict[str, str]) -> None:
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")


PRIORITY_TOPS = {
    "",  # home via index.html
    "solution-for-individuals",
    "solution-for-business-vasps",
    "solution-for-legal-professionals",
    "solution-for-law-enforcement",
    "blockchain-investigations",
    "blockchain-forensic-training",
    "blockchain-investigation-management-system",
    "digital-asset-recovery",
    "source-of-funds-reports",
    "source-of-funds",
    "aftercare-protocol",
    "incident-response-aftercare-protocol",
    "blog",
    "knowledge-center",
    "privacy-policy",
    "terms-and-conditions",
    "impersonation-recovery-scams-warning",
    "newsletter",
    "services",
    "homepage",
    "the-zondacrypto-investigation",
    "asset-recovery",
    "investigations",
    "intelligence",
}


def is_en_page(rel: str) -> bool:
    if rel == "index.html":
        return True
    top = rel.split("/")[0]
    if any(top.startswith(p) for p in SKIP_PREFIXES):
        return False
    # Priority: main nav / service / legal pages only (blog listing, not every post)
    if top in PRIORITY_TOPS:
        # for blog: only listing page, not every article yet
        if top == "blog":
            return rel == "blog/index.html"
        return True
    return False


def is_english(t: str) -> bool:
    if len(t) < 12:
        # allow important short UI
        if t in FIXED:
            return True
        if len(t) < 8:
            return False
    if t in KEEP:
        return False
    if NAME_RE.match(t) and len(t.split()) <= 4:
        return False
    if not re.search(r"[A-Za-z]{4,}", t):
        return False
    lat = len(re.findall(r"[A-Za-z]", t))
    cyr = len(re.findall(r"[А-Яа-яЁё]", t))
    if cyr >= lat:
        return False
    if t.startswith(("http", "www", "/", "#", "{", "function", "var ", "const ")):
        return False
    # require at least one space OR length>=20 (sentences / labels)
    if " " not in t and len(t) < 20 and t not in FIXED:
        return False
    return True


def collect(html: str) -> list[str]:
    p = TextCollector()
    try:
        p.feed(html)
    except Exception:
        return []
    out = []
    seen = set()
    for t in p.texts:
        if t in seen:
            continue
        if is_english(t):
            seen.add(t)
            out.append(t)
    return out


def translate_one(text: str, cache: dict[str, str]) -> str:
    if text in FIXED:
        cache[text] = FIXED[text]
        return FIXED[text]
    if text in KEEP:
        cache[text] = text
        return text
    if text in cache and cache[text]:
        return cache[text]

    for attempt in range(5):
        try:
            ru = ts.translate_text(
                text[:4500],
                translator="bing",
                from_language="en",
                to_language="ru",
            )
            cache[text] = ru
            time.sleep(0.08)
            return ru
        except Exception:
            time.sleep(0.8 + attempt * 0.5)
            try:
                ru = ts.translate_text(
                    text[:4500],
                    translator="google",
                    from_language="en",
                    to_language="ru",
                )
                cache[text] = ru
                time.sleep(0.2)
                return ru
            except Exception as e:
                if attempt == 4:
                    print(f"FAIL {text[:70]!r}: {e}", flush=True)
                    cache[text] = text
                    return text
    return text


def apply_map(html: str, mapping: dict[str, str]) -> str:
    for en in sorted(mapping.keys(), key=len, reverse=True):
        ru = mapping[en]
        if en and ru and en != ru and en in html:
            html = html.replace(en, ru)
    return html


def main() -> None:
    cache = load_cache()
    cache.update(FIXED)

    pages = []
    for p in sorted(MAIN.rglob("index.html")):
        rel = p.relative_to(MAIN).as_posix()
        if is_en_page(rel):
            pages.append(p)

    print(f"pages={len(pages)} cache={len(cache)}", flush=True)

    strings: list[str] = []
    seen: set[str] = set()
    for p in pages:
        html = p.read_text(encoding="utf-8", errors="replace")
        for s in collect(html):
            if s not in seen:
                seen.add(s)
                strings.append(s)

    print(f"unique EN strings={len(strings)}", flush=True)

    mapping: dict[str, str] = {}
    for i, s in enumerate(strings, 1):
        mapping[s] = translate_one(s, cache)
        if i % 15 == 0 or i == len(strings):
            print(f"[{i}/{len(strings)}] cache={len(cache)}", flush=True)
            save_cache(cache)

    save_cache(cache)

    # Apply to all pages so shared header/footer update everywhere
    changed = 0
    for p in sorted(MAIN.rglob("index.html")):
        html = p.read_text(encoding="utf-8", errors="replace")
        new = apply_map(html, mapping)
        new = apply_map(new, FIXED)
        if new != html:
            p.write_text(new, encoding="utf-8")
            changed += 1
    print(f"DONE files={changed} translations={sum(1 for k,v in mapping.items() if k!=v)}", flush=True)


if __name__ == "__main__":
    main()
