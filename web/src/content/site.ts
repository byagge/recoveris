/** Site-wide settings — edit here to update branding, CTAs, and links. */
export const site = {
  name: "Recoveris",
  legalName: "Recoveris AG",
  tagline: "Agentic investigations for the on-chain economy",
  url: "https://recoveris.io",
  email: "contact@recoveris.io",
  address: {
    street: "Poststrasse 24",
    city: "6300 Zug",
    country: "Switzerland",
  },
  social: {
    linkedin: "https://www.linkedin.com/company/recoveris/",
    x: "https://x.com/RecoverisTeam",
    youtube: "https://www.youtube.com/@recoveris",
  },
  cta: {
    label: "Start Your Recovery",
    href: "https://my.recoveris.io/wizard?source=Website_WW_solution-for-individuals&lang=EN",
  },
  headerCta: {
    label: "RECOVER YOUR FUNDS",
    href: "https://my.recoveris.io/wizard?source=Website_WW_solution-for-individuals&lang=EN",
  },
  copyright: "© 2026 Recoveris. All rights reserved.",
  footerLinks: [
    { label: "Terms & Conditions", href: "https://recoveris.io/terms-and-conditions" },
    { label: "Privacy Policy", href: "https://recoveris.io/privacy-policy" },
  ],
} as const;
