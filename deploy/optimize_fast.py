#!/usr/bin/env python3
"""Fast path: local Manrope fonts, strip blockers, gzip-ready HTML, RU dictionary."""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

ROOT = Path(r"d:\codes\recoveris.io")
MAIN = ROOT / "main"
FONTS = MAIN / "fonts"
FONTS.mkdir(parents=True, exist_ok=True)

FONT_FILES = {
    "manrope-cyrillic-400.woff2": "https://cdn.jsdelivr.net/fontsource/fonts/manrope@5.2.5/cyrillic-400-normal.woff2",
    "manrope-cyrillic-500.woff2": "https://cdn.jsdelivr.net/fontsource/fonts/manrope@5.2.5/cyrillic-500-normal.woff2",
    "manrope-cyrillic-600.woff2": "https://cdn.jsdelivr.net/fontsource/fonts/manrope@5.2.5/cyrillic-600-normal.woff2",
    "manrope-cyrillic-700.woff2": "https://cdn.jsdelivr.net/fontsource/fonts/manrope@5.2.5/cyrillic-700-normal.woff2",
    "manrope-latin-400.woff2": "https://cdn.jsdelivr.net/fontsource/fonts/manrope@5.2.5/latin-400-normal.woff2",
    "manrope-latin-500.woff2": "https://cdn.jsdelivr.net/fontsource/fonts/manrope@5.2.5/latin-500-normal.woff2",
    "manrope-latin-600.woff2": "https://cdn.jsdelivr.net/fontsource/fonts/manrope@5.2.5/latin-600-normal.woff2",
    "manrope-latin-700.woff2": "https://cdn.jsdelivr.net/fontsource/fonts/manrope@5.2.5/latin-700-normal.woff2",
    "manrope-latin-ext-400.woff2": "https://cdn.jsdelivr.net/fontsource/fonts/manrope@5.2.5/latin-ext-400-normal.woff2",
    "manrope-latin-ext-500.woff2": "https://cdn.jsdelivr.net/fontsource/fonts/manrope@5.2.5/latin-ext-500-normal.woff2",
    "manrope-latin-ext-600.woff2": "https://cdn.jsdelivr.net/fontsource/fonts/manrope@5.2.5/latin-ext-600-normal.woff2",
    "manrope-latin-ext-700.woff2": "https://cdn.jsdelivr.net/fontsource/fonts/manrope@5.2.5/latin-ext-700-normal.woff2",
}

FONT_CSS = """
@font-face{font-family:'Manrope';font-style:normal;font-weight:400;font-display:swap;src:url('../fonts/manrope-cyrillic-400.woff2') format('woff2'),url('../fonts/manrope-latin-ext-400.woff2') format('woff2'),url('../fonts/manrope-latin-400.woff2') format('woff2')}
@font-face{font-family:'Manrope';font-style:normal;font-weight:500;font-display:swap;src:url('../fonts/manrope-cyrillic-500.woff2') format('woff2'),url('../fonts/manrope-latin-ext-500.woff2') format('woff2'),url('../fonts/manrope-latin-500.woff2') format('woff2')}
@font-face{font-family:'Manrope';font-style:normal;font-weight:600;font-display:swap;src:url('../fonts/manrope-cyrillic-600.woff2') format('woff2'),url('../fonts/manrope-latin-ext-600.woff2') format('woff2'),url('../fonts/manrope-latin-600.woff2') format('woff2')}
@font-face{font-family:'Manrope';font-style:normal;font-weight:700;font-display:swap;src:url('../fonts/manrope-cyrillic-700.woff2') format('woff2'),url('../fonts/manrope-latin-ext-700.woff2') format('woff2'),url('../fonts/manrope-latin-700.woff2') format('woff2')}
html,body{font-family:Manrope,system-ui,-apple-system,"Segoe UI",sans-serif!important;letter-spacing:0.01em;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
h1,h2,h3,h4,.header-link,.btn{font-family:Manrope,system-ui,sans-serif!important;letter-spacing:-0.01em}
"""

# Longest-first applied dictionary (UI + homepage + service heroes)
RU: dict[str, str] = {
    "Recoveris - Agentic investigations for the on-chain economy": "Recoveris — Агентные расследования для on-chain экономики",
    "Built by investigators and legal professionals, Recoveris combines deep human expertise with AI-driven technology to deliver advanced intelligence, investigations, recovery, and compliance solutions for digital assets.": "Команда следователей и юристов сочетает экспертизу людей и AI для разведки, расследований, возврата активов и комплаенса в сфере цифровых активов.",
    "The future of finance is tokenized. The future of investigations is agentic. We operate at the intersection.": "Будущее финансов — токенизировано. Будущее расследований — агентное. Мы работаем на их пересечении.",
    "We collaborate with public and private institutions globally to provide effective prevention and aftercare support for digital asset linked crime.": "Мы сотрудничаем с государственными и частными институтами по всему миру, обеспечивая профилактику и aftercare-поддержку при преступлениях, связанных с цифровыми активами.",
    "We serve diverse clients, delivering blockchain investigation and recovery solutions that help with returning lost or stolen digital assets to their rightful owners.": "Мы работаем с разными клиентами и предоставляем блокчейн-расследования и решения по возврату утраченных или украденных цифровых активов их законным владельцам.",
    "Digital asset risk moves fast. Make sure your organization is prepared": "Риски цифровых активов меняются быстро. Подготовьте организацию",
    "Your crypto was stolen, but it’s not gone": "Вашу криптовалюту украли — но она не исчезла",
    "Your crypto was stolen, but it's not gone": "Вашу криптовалюту украли — но она не исчезла",
    "Enforcement-ready evidence and expert intelligence for digital assets": "Доказательства и экспертная разведка для дел с цифровыми активами",
    "Your cases involve blockchain. So should your forensic capabilities": "Если дела связаны с блокчейном — нужны и форензик-возможности",
    "Blockchain intelligence workflow for professionals in digital assets": "Интеллект-workflow для профессионалов цифровых активов",
    "Aftercare Protocol that sets new industry standards": "Aftercare Protocol, задающий отраслевой стандарт",
    "Has your crypto been stolen? We can help": "Украли криптовалюту? Мы можем помочь",
    "Defensible provenance reports that hold up in court": "Доказуемые отчёты о происхождении средств для суда",
    "Blockchain forensics for complex and high-stake cases": "Блокчейн-форензика для сложных и высокорисковых дел",
    "Investigative expertise taught by active practitioners": "Следственная экспертиза от практикующих специалистов",
    "Trusted by global institutions": "Нам доверяют институты по всему миру",
    "Trusted by <span>global institutions</span>": "Нам доверяют <span>институты по всему миру</span>",
    "Trusted by": "Нам доверяют",
    "global institutions": "институты по всему миру",
    "How we help our clients": "Как мы помогаем клиентам",
    "How we help <span>our clients</span>": "Как мы помогаем <span>клиентам</span>",
    "Who we help": "Кому помогаем",
    "Who we serve": "Кого мы обслуживаем",
    "About Recoveris": "О Recoveris",
    "The Recoveris team": "Команда Recoveris",
    "Case studies": "Кейсы",
    "Contact our team": "Связаться с командой",
    "Connect with our team": "Связаться с нашей командой",
    "Begin Your Recovery": "Начните возврат средств",
    "Our recovery framework": "Наш фреймворк возврата",
    "Our recent posts": "Недавние публикации",
    "Our videos": "Наши видео",
    "Recoveris in media": "Recoveris в СМИ",
    "Member of elite associations": "Участник ведущих ассоциаций",
    "Associations": "Ассоциации",
    "Transforming blockchain intelligence into results": "Превращаем блокчейн-разведку в результат",
    "Traditional Finance Institutions": "Традиционные финансовые институты",
    "Founders": "Основатели",
    "EY × Recoveris Distributed Ledger Analysis product": "EY × Recoveris — продукт Distributed Ledger Analysis",
    "1inch — Tracing USD 2.2M Through Tornado Cash": "1inch — трассировка USD 2.2M через Tornado Cash",
    "1inch: Tracing USD 2.2M Through Tornado Cash": "1inch: трассировка USD 2.2M через Tornado Cash",
    "Upbit — USD 35M+ Multi-Chain Laundering Disrupted": "Upbit — прервано отмывание USD 35M+ по нескольким сетям",
    "Upbit Exchange Hot Wallet Compromise: USD 35M+ Multi-Chain Laundering Disruption": "Компрометация hot wallet биржи Upbit: прерывание мультичейн-отмывания USD 35M+",
    "Fake VC Impersonation — USD 1.7M+ Recovered": "Импersonация Fake VC — возвращено USD 1.7M+",
    "Fake VC Impersonation: Over USD 1.7M Recovered Across Chains (anonymized)": "Импersonация Fake VC: более USD 1.7M возвращено кросс-чейн (анонимно)",
    "Corporate Phishing (BEC) — USD 40M Wire Fraud": "Корпоративный фишинг (BEC) — wire-мошенничество USD 40M",
    "Corporate Phishing (BEC): Cross-Chain Tracing of a USD 40M Wire Fraud (anonymized)": "Корпоративный фишинг (BEC): кросс-чейн трассировка wire-мошенничества USD 40M (анонимно)",
    "ZondaCrypto — Detecting Exchange Insolvency Early": "ZondaCrypto — раннее выявление несостоятельности биржи",
    "Zondacrypto: Detecting Exchange Insolvency Before Public Collapse": "Zondacrypto: выявление несостоятельности до публичного краха",
    "Swiss Investment Fraud: USD 10.5M Frozen and Returned": "Швейцарское инвестмошенничество: USD 10.5M заморожено и возвращено",
    "INTELLIGENCE": "РАЗВЕДКА",
    "OPERATIONS": "ОПЕРАЦИИ",
    "Our solutions": "Наши решения",
    "--> Our solutions": "Наши решения",
    "RECOVER YOUR FUNDS": "ВЕРНУТЬ СРЕДСТВА",
    "Recover your funds": "Вернуть средства",
    "Terms & Conditions": "Условия использования",
    "Terms &amp; Conditions": "Условия использования",
    "Privacy Policy": "Политика конфиденциальности",
    "Knowledge Center": "База знаний",
    "Impersonation &amp; Recovery Scams Warning": "Предупреждение о скамах с «возвратом»",
    "Impersonation & Recovery Scams Warning": "Предупреждение о скамах с «возвратом»",
    "Blockchain Investigation Management System": "Система управления блокчейн-расследованиями",
    "Source of Funds reports": "Отчёты Source of Funds",
    "Source of funds reports": "Отчёты Source of Funds",
    "Digital Asset Recovery for Victims": "Возврат цифровых активов для пострадавших",
    "Incident Response and Aftercare Protocol": "Реагирование на инциденты и Aftercare Protocol",
    "Tailored Trainings": "Обучение",
    "Asset Recovery": "Возврат активов",
    "Business &amp; VASPs": "Бизнес и VASP",
    "Business & VASPs": "Бизнес и VASP",
    "Legal Professionals": "Юристы",
    "Law Enforcement": "Правоохранение",
    "For Individuals": "Для частных лиц",
    "For Business &amp; VASPs": "Для бизнеса и VASP",
    "For Business & VASPs": "Для бизнеса и VASP",
    "For Legal Professionals": "Для юристов",
    "For Law Enforcement": "Для правоохранения",
    "Solution For Individuals - Recoveris": "Решение для частных лиц — Recoveris",
    "Solution for Business & VASPs - Recoveris": "Решение для бизнеса и VASP — Recoveris",
    "Solution for Legal Professionals - Recoveris": "Решение для юристов — Recoveris",
    "Solution for Law Enforcement - Recoveris": "Решение для правоохранения — Recoveris",
    "Agentic investigations": "Агентные расследования",
    "for the on-chain economy": "для on-chain экономики",
    "Investigations": "Расследования",
    "Individuals": "Частные лица",
    "Services": "Услуги",
    "About": "О компании",
    "Home": "Главная",
    "Blog": "Блог",
    "Contact": "Контакты",
    "Read more": "Читать далее",
    "Learn more": "Подробнее",
    "All rights reserved": "Все права защищены",
    "Newsletter": "Рассылка",
    "Leadership": "Руководство",
    "Intelligence": "Разведка",
    "Operations": "Операции",
    "Product": "Продукт",
    "Media": "СМИ",
    "Partners": "Партнёры",
    "Our team": "Наша команда",
    "Submit": "Отправить",
    "First Name": "Имя",
    "Last Name": "Фамилия",
    "Your message": "Ваше сообщение",
    "Phone number": "Телефон",
    "Company": "Компания",
    "Get in touch": "Связаться",
    "Send message": "Отправить сообщение",
    "Case Study": "Кейс",
    "The challenge:": "Задача:",
    "Our approach:": "Наш подход:",
    "Outcome:": "Результат:",
    "Public coverage:": "Публикации:",
    "Detailed coverage:": "Подробнее:",
    "Read the case study": "Читать кейс",
}


def ensure_fonts() -> None:
    for name, url in FONT_FILES.items():
        dest = FONTS / name
        if dest.exists() and dest.stat().st_size > 1000:
            continue
        print("download", name)
        urllib.request.urlretrieve(url, dest)
    (MAIN / "css" / "manrope.css").write_text(FONT_CSS, encoding="utf-8")
    css_path = MAIN / "css" / "main.11cf34fc32282edf5ca2.css"
    css = css_path.read_text(encoding="utf-8", errors="replace")
    css = re.sub(r"@import url\(https://fonts\.googleapis\.com[^)]+\);\s*", "", css)
    css = css.replace("font-family:Poppins,sans-serif", "font-family:Manrope,system-ui,sans-serif")
    css_path.write_text(css, encoding="utf-8")
    print("fonts+css ready")


def strip_heavy(html: str) -> str:
    patterns = [
        r'<script[^>]+cloudflareinsights\.com[^>]*>\s*</script>',
        r'<script[^>]+id="cookieyes"[^>]*>\s*</script>',
        r'<script[^>]+src="[^"]*gcm\.min\.js"[^>]*>\s*</script>',
        r'<script[^>]+id="cookie-law-info-gcm-var-js"[^>]*>[\s\S]*?</script>',
        r'<script[^>]+src="[^"]*gtm\.js"[^>]*>\s*</script>',
        r'<script[^>]+src="[^"]*js/script\.js"[^>]*>\s*</script>',
        r'<script[^>]+src="[^"]*announcement-[^"]+\.js"[^>]*>\s*</script>',
        r'<script[^>]+src="[^"]*analytics\.js"[^>]*>\s*</script>',
        r'<script[^>]+src="[^"]*google-recaptcha[^"]*"[^>]*>\s*</script>',
        r'<script[^>]+src="[^"]*js/api\.js"[^>]*>\s*</script>',
        r'<link[^>]+dns-prefetch[^>]*>',
        r"<!-- Google Tag Manager[\s\S]*?End Google Tag Manager[^>]*-->",
    ]
    for p in patterns:
        html = re.sub(p, "", html, flags=re.I)
    # defer non-critical bottom scripts
    html = re.sub(
        r"(<script)([^>]*\ssrc=\"[^\"]+\.js\"[^>]*)(>)",
        lambda m: m.group(0)
        if "defer" in m.group(0) or "async" in m.group(0) or "jquery.min" in m.group(0)
        else f'{m.group(1)}{m.group(2)} defer{m.group(3)}',
        html,
        flags=re.I,
    )
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html


def apply_ru(html: str) -> str:
    for en in sorted(RU.keys(), key=len, reverse=True):
        html = html.replace(en, RU[en])
    return html


def inject_font(html: str, depth: int) -> str:
    href = ("../" * depth) + "css/manrope.css" if depth else "css/manrope.css"
    if "css/manrope.css" not in html:
        html = re.sub(r"(</title>)", rf'\1\n<link rel="stylesheet" href="{href}">', html, count=1, flags=re.I)
    html = re.sub(r'(<html[^>]*)\slang=(["\'])[a-z-]+\2', r'\1 lang=\2ru\2', html, count=1, flags=re.I)
    m = re.search(r"<html[^>]*>", html, re.I)
    if m and "lang=" not in m.group(0):
        html = re.sub(r"<html", '<html lang="ru"', html, count=1, flags=re.I)
    return html


def process(path: Path) -> None:
    rel = path.relative_to(MAIN)
    depth = len(rel.parts) - 1
    html = path.read_text(encoding="utf-8", errors="replace")
    before = len(html)
    html = strip_heavy(html)
    html = apply_ru(html)
    html = inject_font(html, depth)
    path.write_text(html, encoding="utf-8")
    print(f"OK {rel} {before}->{len(html)}")


def main() -> None:
    ensure_fonts()
    pages = sorted(MAIN.rglob("index.html"))
    print("pages", len(pages))
    for p in pages:
        process(p)
    print("DONE")


if __name__ == "__main__":
    main()
