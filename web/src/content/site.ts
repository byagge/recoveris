/** Настройки сайта — меняйте бренд, CTA и ссылки здесь. */
export const site = {
  name: "Recoveris",
  legalName: "Recoveris AG",
  tagline: "Агентные расследования для on-chain экономики",
  url: "/",
  email: "contact@recoveris.arix.vu",
  address: {
    street: "Poststrasse 24",
    city: "6300 Zug",
    country: "Швейцария",
  },
  social: {
    linkedin: "#",
    x: "#",
    youtube: "#",
  },
  cta: {
    label: "Начать возврат средств",
    href: "/contact",
  },
  headerCta: {
    label: "ВЕРНУТЬ СРЕДСТВА",
    href: "/contact",
  },
  copyright: "© 2026 Recoveris. Все права защищены.",
  footerLinks: [
    { label: "Условия использования", href: "/terms" },
    { label: "Политика конфиденциальности", href: "/privacy" },
  ],
} as const;
