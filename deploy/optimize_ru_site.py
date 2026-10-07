#!/usr/bin/env python3
"""Speed up static mirror + switch UI/content to Russian + local Cyrillic fonts."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString
from deep_translator import MyMemoryTranslator

ROOT = Path(r"d:\codes\recoveris.io")
MAIN = ROOT / "main"
CACHE_PATH = ROOT / "_pages" / "translate_cache.json"
CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)

# Manual high-quality UI / marketing phrases (longest first later)
UI = {
    "Agentic investigations for the on-chain economy": "Агентные расследования для on-chain экономики",
    "The future of finance is tokenized. The future of investigations is agentic. We operate at the intersection.": "Будущее финансов — токенизировано. Будущее расследований — агентное. Мы работаем на их пересечении.",
    "Built by investigators and legal professionals, Recoveris combines deep human expertise with AI-driven technology to deliver advanced intelligence, investigations, recovery, and compliance solutions for digital assets.": "Команда следователей и юристов сочетает экспертизу людей и AI для разведки, расследований, возврата активов и комплаенса в сфере цифровых активов.",
    "We collaborate with public and private institutions globally to provide effective prevention and aftercare support for digital asset linked crime.": "Мы сотрудничаем с государственными и частными институтами по всему миру, обеспечивая профилактику и aftercare-поддержку при преступлениях, связанных с цифровыми активами.",
    "Trusted by global institutions": "Нам доверяют институты по всему миру",
    "Who we help": "Кому помогаем",
    "How we help our clients": "Как мы помогаем клиентам",
    "Who we serve": "Кого мы обслуживаем",
    "About Recoveris": "О Recoveris",
    "The Recoveris team": "Команда Recoveris",
    "Case studies": "Кейсы",
    "Contact our team": "Связаться с командой",
    "RECOVER YOUR FUNDS": "ВЕРНУТЬ СРЕДСТВА",
    "Recover your funds": "Вернуть средства",
    "Terms & Conditions": "Условия использования",
    "Terms &amp; Conditions": "Условия использования",
    "Privacy Policy": "Политика конфиденциальности",
    "Knowledge Center": "База знаний",
    "Impersonation & Recovery Scams Warning": "Предупреждение о скамах с имперсонацией и «возвратом»",
    "Impersonation &amp; Recovery Scams Warning": "Предупреждение о скамах с имперсонацией и «возвратом»",
    "Blockchain Investigation Management System": "Система управления блокчейн-расследованиями",
    "Aftercare Protocol": "Aftercare Protocol",
    "Asset Recovery": "Возврат активов",
    "Source of Funds reports": "Отчёты Source of Funds",
    "Source of funds reports": "Отчёты Source of Funds",
    "Tailored Trainings": "Обучение",
    "Investigations": "Расследования",
    "Business & VASPs": "Бизнес и VASP",
    "Business &amp; VASPs": "Бизнес и VASP",
    "Legal Professionals": "Юристы",
    "Law Enforcement": "Правоохранение",
    "For Individuals": "Для частных лиц",
    "For Business & VASPs": "Для бизнеса и VASP",
    "For Business &amp; VASPs": "Для бизнеса и VASP",
    "For Legal Professionals": "Для юристов",
    "For Law Enforcement": "Для правоохранения",
    "Digital Asset Recovery for Victims": "Возврат цифровых активов для пострадавших",
    "Incident Response and Aftercare Protocol": "Реагирование на инциденты и Aftercare Protocol",
    "Investigative expertise taught by active practitioners": "Следственная экспертиза от практикующих специалистов",
    "Digital asset risk moves fast. Make sure your organization is prepared": "Риски цифровых активов меняются быстро. Подготовьте организацию",
    "Your crypto was stolen, but it’s not gone": "Вашу криптовалюту украли — но она не исчезла",
    "Your crypto was stolen, but it's not gone": "Вашу криптовалюту украли — но она не исчезла",
    "Enforcement-ready evidence and expert intelligence for digital assets": "Доказательства и экспертная разведка для дел с цифровыми активами",
    "Your cases involve blockchain. So should your forensic capabilities": "Если дела связаны с блокчейном — нужны и форензик-возможности",
    "Has your crypto been stolen? We can help": "Украли криптовалюту? Мы можем помочь",
    "Defensible provenance reports that hold up in court": "Доказуемые отчёты о происхождении средств для суда",
    "Blockchain forensics for complex and high-stake cases": "Блокчейн-форензика для сложных и высокорисковых дел",
    "Blockchain intelligence workflow for professionals in digital assets": "Интеллект-workflow для профессионалов цифровых активов",
    "Aftercare Protocol that sets new industry standards": "Aftercare Protocol, задающий отраслевой стандарт",
    "Home": "Главная",
    "About": "О компании",
    "Services": "Услуги",
    "Blog": "Блог",
    "Contact": "Контакты",
    "FAQ": "FAQ",
    "Read more": "Читать далее",
    "Learn more": "Подробнее",
    "Get started": "Начать",
    "Submit": "Отправить",
    "Name": "Имя",
    "Email": "Email",
    "Message": "Сообщение",
    "Phone": "Телефон",
    "All rights reserved": "Все права защищены",
    "Newsletter": "Рассылка",
    "Our solutions": "Наши решения",
    "Our team": "Наша команда",
    "Leadership": "Руководство",
    "Intelligence": "Разведка",
    "Operations": "Операции",
    "Product": "Продукт",
    "Media": "СМИ",
    "Partners": "Партнёры",
    "Individuals": "Частные лица",
}

SKIP_TAGS = {"script", "style", "noscript", "code", "pre", "svg", "path"}
LATIN_RE = re.compile(r"[A-Za-z]")
CYR_RE = re.compile(r"[А-Яа-яЁё]")

FONT_CSS = """
@font-face{font-family:'Manrope';font-style:normal;font-weight:400;font-display:swap;
  src:url('../fonts/manrope-cyrillic-400.woff2') format('woff2'),url('../fonts/manrope-latin-ext-400.woff2') format('woff2'),url('../fonts/manrope-latin-400.woff2') format('woff2')}
@font-face{font-family:'Manrope';font-style:normal;font-weight:500;font-display:swap;
  src:url('../fonts/manrope-cyrillic-500.woff2') format('woff2'),url('../fonts/manrope-latin-ext-500.woff2') format('woff2'),url('../fonts/manrope-latin-500.woff2') format('woff2')}
@font-face{font-family:'Manrope';font-style:normal;font-weight:600;font-display:swap;
  src:url('../fonts/manrope-cyrillic-600.woff2') format('woff2'),url('../fonts/manrope-latin-ext-600.woff2') format('woff2'),url('../fonts/manrope-latin-600.woff2') format('woff2')}
@font-face{font-family:'Manrope';font-style:normal;font-weight:700;font-display:swap;
  src:url('../fonts/manrope-cyrillic-700.woff2') format('woff2'),url('../fonts/manrope-latin-ext-700.woff2') format('woff2'),url('../fonts/manrope-latin-700.woff2') format('woff2')}
"""

def load_cache() -> dict[str, str]:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict[str, str]) -> None:
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")


def patch_main_css() -> None:
    css_path = MAIN / "css" / "main.11cf34fc32282edf5ca2.css"
    css = css_path.read_text(encoding="utf-8", errors="replace")
    css = re.sub(
        r"@import url\(https://fonts\.googleapis\.com[^)]+\);",
        "",
        css,
        count=1,
    )
    css = css.replace("font-family:Poppins,sans-serif", "font-family:Manrope,system-ui,sans-serif")
    css = css.replace("font-family: Poppins, sans-serif", "font-family: Manrope, system-ui, sans-serif")
    # url() is relative to this CSS file in css/ → ../fonts/
    (MAIN / "css" / "manrope.css").write_text(FONT_CSS, encoding="utf-8")
    css_path.write_text(css, encoding="utf-8")
    print("patched main CSS fonts")


def strip_heavy(html: str) -> str:
    # Remove cloudflare beacon / cookieyes / gtm remote beacons
    html = re.sub(
        r'<script[^>]+cloudflareinsights\.com[^>]*>\s*</script>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<script[^>]+id="cookieyes"[^>]*>\s*</script>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<script[^>]+src="[^"]*gcm\.min\.js"[^>]*>\s*</script>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<script[^>]+id="cookie-law-info-gcm-var-js"[^>]*>[\s\S]*?</script>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<script[^>]+src="[^"]*gtm\.js"[^>]*>\s*</script>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<script[^>]+src="[^"]*js/script\.js"[^>]*>\s*</script>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<script[^>]+src="[^"]*announcement-[^"]+\.js"[^>]*>\s*</script>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<script[^>]+src="[^"]*analytics\.js"[^>]*>\s*</script>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<link[^>]+dns-prefetch[^>]*>',
        "",
        html,
        flags=re.I,
    )
    # Collapse runs of blank lines (some pages doubled size)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html


def inject_font_link(html: str, depth: int) -> str:
    href = ("../" * depth) + "css/manrope.css" if depth else "css/manrope.css"
    link = f'<link rel="stylesheet" href="{href}">'
    html = re.sub(r"(<html[^>]*)\slang=(['\"])[a-z-]+\2", r"\1 lang=\2ru\2", html, count=1, flags=re.I)
    m = re.search(r"<html[^>]*>", html, re.I)
    if m and "lang=" not in m.group(0):
        html = re.sub(r"<html", '<html lang="ru"', html, count=1, flags=re.I)
    if "css/manrope.css" not in html:
        html = re.sub(r"(</title>)", r"\1\n" + link, html, count=1, flags=re.I)
    return html


def apply_ui(html: str) -> str:
    # longest keys first
    for en in sorted(UI.keys(), key=len, reverse=True):
        html = html.replace(en, UI[en])
    return html


def should_translate(text: str) -> bool:
    t = text.strip()
    if len(t) < 3:
        return False
    if not LATIN_RE.search(t):
        return False
    if CYR_RE.search(t) and not re.search(r"[A-Za-z]{4,}", t):
        return False
    # skip urls / emails / pure codes
    if t.startswith(("http", "www.", "/", "#", "{", "[")):
        return False
    if "@" in t and "." in t and " " not in t:
        return False
    if re.fullmatch(r"[\d\s\.\,\$\%€£¥+\-–—/:]+", t):
        return False
    return True


def translate_text(text: str, cache: dict[str, str], translator: MyMemoryTranslator) -> str:
    key = text.strip()
    if key in cache:
        return cache[key]
    if key in UI:
        cache[key] = UI[key]
        return UI[key]
    # Keep leading/trailing whitespace
    lead = re.match(r"^\s*", text).group(0)
    trail = re.search(r"\s*$", text).group(0)
    body = text.strip()
    try:
        # MyMemory max ~500 chars
        if len(body) > 450:
            parts = re.split(r"(?<=[\.\!\?])\s+", body)
            out_parts = []
            buf = ""
            for p in parts:
                if len(buf) + len(p) < 450:
                    buf = f"{buf} {p}".strip()
                else:
                    if buf:
                        out_parts.append(translator.translate(buf))
                        time.sleep(0.35)
                    buf = p
            if buf:
                out_parts.append(translator.translate(buf))
                time.sleep(0.35)
            translated = " ".join(out_parts)
        else:
            translated = translator.translate(body)
            time.sleep(0.3)
        cache[key] = translated
        return lead + translated + trail
    except Exception as e:
        print(f"  translate fail: {e!s:.80}")
        cache[key] = body  # avoid retry storm
        return text


def collect_visible_strings(html: str) -> list[str]:
    """Find visible English snippets without rewriting the document."""
    soup = BeautifulSoup(html, "html.parser")
    found: list[str] = []
    seen: set[str] = set()
    for node in soup.find_all(string=True):
        if not isinstance(node, NavigableString):
            continue
        parent = node.parent
        if parent is None or parent.name in SKIP_TAGS:
            continue
        raw = str(node)
        key = raw.strip()
        if not key or key in seen or not should_translate(raw):
            continue
        seen.add(key)
        found.append(key)
    # title + meta
    if soup.title and soup.title.string:
        t = soup.title.string.strip()
        if t and t not in seen and should_translate(t):
            found.append(t)
    for meta in soup.find_all("meta", attrs={"name": "description"}):
        c = (meta.get("content") or "").strip()
        if c and c not in seen and should_translate(c):
            found.append(c)
    return found


def apply_translations(html: str, mapping: dict[str, str]) -> str:
    for en in sorted(mapping.keys(), key=len, reverse=True):
        ru = mapping[en]
        if en and ru and en != ru:
            html = html.replace(en, ru)
    return html


# Core pages get full MT; others get UI dict + strip only (SEO foreign pages stay until later)
CORE_GLOBS = [
    "index.html",
    "solution-for-*/index.html",
    "blockchain-*/index.html",
    "digital-asset-recovery/index.html",
    "source-of-funds-reports/index.html",
    "aftercare-protocol/index.html",
    "blog/index.html",
    "knowledge-center/index.html",
    "privacy-policy/index.html",
    "terms-and-conditions/index.html",
    "impersonation-recovery-scams-warning/index.html",
    "newsletter/index.html",
    "homepage/index.html",
    "services/index.html",
]


def is_core(path: Path) -> bool:
    rel = path.relative_to(MAIN).as_posix()
    if rel == "index.html":
        return True
    core_dirs = {
        "solution-for-individuals",
        "solution-for-business-vasps",
        "solution-for-legal-professionals",
        "solution-for-law-enforcement",
        "blockchain-investigations",
        "blockchain-forensic-training",
        "blockchain-investigation-management-system",
        "digital-asset-recovery",
        "source-of-funds-reports",
        "aftercare-protocol",
        "blog",
        "knowledge-center",
        "privacy-policy",
        "terms-and-conditions",
        "impersonation-recovery-scams-warning",
        "newsletter",
        "services",
        "homepage",
        "contact",
    }
    parts = rel.split("/")
    return parts[0] in core_dirs


def depth_of(path: Path) -> int:
    rel = path.relative_to(MAIN)
    return len(rel.parts) - 1


def process_file(path: Path, cache: dict[str, str], translator: MyMemoryTranslator) -> None:
    html = path.read_text(encoding="utf-8", errors="replace")
    depth = depth_of(path)
    html = strip_heavy(html)
    html = apply_ui(html)
    html = inject_font_link(html, depth)

    if is_core(path):
        mapping: dict[str, str] = {}
        try:
            strings = collect_visible_strings(html)
        except Exception as e:
            print(f"  collect fail: {e}")
            strings = []
        print(f"  strings={len(strings)}")
        for s in strings:
            if s in UI:
                mapping[s] = UI[s]
            elif s in cache:
                mapping[s] = cache[s]
            else:
                mapping[s] = translate_text(s, cache, translator)
        html = apply_translations(html, mapping)

    html = apply_ui(html)
    path.write_text(html, encoding="utf-8")


def main() -> None:
    patch_main_css()
    cache = load_cache()
    translator = MyMemoryTranslator(source="en-GB", target="ru-RU")
    pages = sorted(MAIN.rglob("index.html"))
    # Process core first (full MT), then the rest (UI only)
    cores = [p for p in pages if is_core(p)]
    others = [p for p in pages if not is_core(p)]
    ordered = cores + others
    print(f"pages={len(pages)} core={len(cores)} cache={len(cache)}")
    for i, path in enumerate(ordered, 1):
        core = is_core(path)
        print(f"[{i}/{len(ordered)}] {'CORE' if core else 'ui  '} {path.relative_to(MAIN)}")
        process_file(path, cache, translator)
        if i % 5 == 0:
            save_cache(cache)
    save_cache(cache)
    print(f"DONE cache={len(cache)}")


if __name__ == "__main__":
    main()
