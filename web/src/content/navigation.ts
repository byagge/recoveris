/** Header navigation — edit labels, URLs, and submenu items here. */
export type NavLink = {
  label: string;
  href?: string;
  children?: { label: string; href: string }[];
};

export const navigation: NavLink[] = [
  { label: "Home", href: "https://recoveris.io/" },
  {
    label: "About",
    children: [
      { label: "About Recoveris", href: "https://recoveris.io/#about" },
      { label: "The Recoveris team", href: "https://recoveris.io/#team" },
      { label: "Case studies", href: "https://recoveris.io/#casestudies" },
      { label: "FAQ", href: "https://recoveris.io/#faq" },
      { label: "Contact", href: "https://recoveris.io/#contact" },
    ],
  },
  {
    label: "Who we help",
    children: [
      { label: "Individuals", href: "/" },
      {
        label: "Business & VASPs",
        href: "https://recoveris.io/solution-for-business-vasps/",
      },
      {
        label: "Legal Professionals",
        href: "https://recoveris.io/solution-for-legal-professionals/",
      },
      {
        label: "Law Enforcement",
        href: "https://recoveris.io/solution-for-law-enforcement/",
      },
    ],
  },
  {
    label: "Services",
    children: [
      {
        label: "Blockchain Investigation Management System",
        href: "https://recoveris.io/blockchain-investigation-management-system/",
      },
      {
        label: "Investigations",
        href: "https://recoveris.io/blockchain-investigations/",
      },
      {
        label: "Asset Recovery",
        href: "https://recoveris.io/digital-asset-recovery/",
      },
      {
        label: "Source of Funds reports",
        href: "https://recoveris.io/source-of-funds-reports/",
      },
      {
        label: "Aftercare Protocol",
        href: "https://recoveris.io/aftercare-protocol/",
      },
      {
        label: "Tailored Trainings",
        href: "https://recoveris.io/blockchain-forensic-training/",
      },
    ],
  },
  { label: "Blog", href: "https://recoveris.io/blog" },
  { label: "Knowledge Center", href: "https://recoveris.io/knowledge-center/" },
];
