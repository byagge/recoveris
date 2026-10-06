import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { MarketingPageView } from "@/components/sections/MarketingPageView";
import { marketingPages } from "@/content/pages";

type Props = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return marketingPages.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const page = marketingPages.find((p) => p.slug === slug);
  if (!page) return {};
  return {
    title: page.metaTitle,
    description: page.metaDescription,
  };
}

export default async function MarketingRoute({ params }: Props) {
  const { slug } = await params;
  const page = marketingPages.find((p) => p.slug === slug);
  if (!page) notFound();
  return <MarketingPageView page={page} />;
}
