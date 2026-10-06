import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { blogPosts } from "@/content/pages";
import { site } from "@/content/site";

type Props = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return blogPosts.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const post = blogPosts.find((p) => p.slug === slug);
  return { title: post?.title ?? "Блог" };
}

export default async function BlogPostPage({ params }: Props) {
  const { slug } = await params;
  const post = blogPosts.find((p) => p.slug === slug);
  if (!post) notFound();

  return (
    <main className="page-template-services">
      <section className="main" style={{ paddingBottom: 80 }}>
        <div className="container" style={{ maxWidth: 800 }}>
          <p style={{ color: "var(--yellow)" }}>{post.date}</p>
          <h1 style={{ margin: "12px 0 24px" }}>{post.title}</h1>
          <p>{post.excerpt}</p>
          <p>
            Полная версия статьи готовится. Свяжитесь с нами, если тема
            актуальна для вашего кейса — поможем с разбором.
          </p>
          <div style={{ display: "flex", gap: 20, marginTop: 32, flexWrap: "wrap" }}>
            <Button href={site.cta.href}>{site.cta.label}</Button>
            <Link href="/blog" style={{ color: "var(--yellow)", alignSelf: "center" }}>
              ← Все статьи
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}
