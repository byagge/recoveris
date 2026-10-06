import type { Metadata } from "next";
import { LegalPageView } from "@/components/sections/LegalPageView";
import { legalPages } from "@/content/pages";

export const metadata: Metadata = {
  title: legalPages.scamWarning.title,
};

export default function ScamWarningPage() {
  return <LegalPageView {...legalPages.scamWarning} />;
}
