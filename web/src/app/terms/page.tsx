import type { Metadata } from "next";
import { LegalPageView } from "@/components/sections/LegalPageView";
import { legalPages } from "@/content/pages";

export const metadata: Metadata = {
  title: legalPages.terms.title,
};

export default function TermsPage() {
  return <LegalPageView {...legalPages.terms} />;
}
