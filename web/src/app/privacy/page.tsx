import type { Metadata } from "next";
import { LegalPageView } from "@/components/sections/LegalPageView";
import { legalPages } from "@/content/pages";

export const metadata: Metadata = {
  title: legalPages.privacy.title,
};

export default function PrivacyPage() {
  return <LegalPageView {...legalPages.privacy} />;
}
