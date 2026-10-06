import type { Metadata } from "next";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { home } from "@/content/pages";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: home.metaTitle,
    template: "%s — Recoveris",
  },
  description: home.metaDescription,
  icons: {
    icon: "/favicon.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru">
      <body>
        <Header />
        {children}
        <Footer />
      </body>
    </html>
  );
}
