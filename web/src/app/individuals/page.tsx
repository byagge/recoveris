import type { Metadata } from "next";
import { IndividualsPageView } from "@/components/sections/IndividualsPageView";
import { pageMeta } from "@/content/individuals";

export const metadata: Metadata = {
  title: pageMeta.title,
  description: pageMeta.description,
};

export default function IndividualsPage() {
  return <IndividualsPageView />;
}
