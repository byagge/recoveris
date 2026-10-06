/** Навигация — все ссылки локальные. */
export type NavLink = {
  label: string;
  href?: string;
  children?: { label: string; href: string }[];
};

export const navigation: NavLink[] = [
  { label: "Главная", href: "/" },
  {
    label: "О компании",
    children: [
      { label: "О Recoveris", href: "/#about" },
      { label: "Команда", href: "/#team" },
      { label: "Кейсы", href: "/#casestudies" },
      { label: "FAQ", href: "/#faq" },
      { label: "Контакты", href: "/contact" },
    ],
  },
  {
    label: "Кому помогаем",
    children: [
      { label: "Частные лица", href: "/individuals" },
      { label: "Бизнес и VASP", href: "/business" },
      { label: "Юристы", href: "/legal" },
      { label: "Правоохранительные органы", href: "/law-enforcement" },
    ],
  },
  {
    label: "Услуги",
    children: [
      { label: "Система управления расследованиями (BIMS)", href: "/bims" },
      { label: "Расследования", href: "/investigations" },
      { label: "Возврат активов", href: "/recovery" },
      { label: "Отчёты Source of Funds", href: "/source-of-funds" },
      { label: "Aftercare Protocol", href: "/aftercare" },
      { label: "Обучение", href: "/training" },
    ],
  },
  { label: "Блог", href: "/blog" },
  { label: "База знаний", href: "/knowledge-center" },
];
