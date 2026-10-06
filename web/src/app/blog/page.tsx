import type { Metadata } from "next";
import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { blogPosts } from "@/content/pages";
import { site } from "@/content/site";

export const metadata: Metadata = {
  title: "Блог",
  description: "Статьи о блокчейн-расследованиях, возврате активов и комплаенсе.",
};

export default function BlogPage() {
  return (
    <main className="page-template-services">
      <section className="main" style={{ paddingBottom: 80 }}>
        <div className="container">
          <h1 style={{ marginBottom: 16 }}>
            Блог <span>Recoveris</span>
          </h1>
          <p style={{ marginBottom: 48, maxWidth: 640 }}>
            Материалы о форензике, возврате активов и регулировании.
          </p>
          <div
            className="services-wrapper"
            style={{
              gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
              marginTop: 0,
            }}
          >
            {blogPosts.map((post) => (
              <article className="services-item" key={post.slug}>
                <p style={{ color: "var(--yellow)", margin: "0 0 8px" }}>
                  {post.date}
                </p>
                <h3>{post.title}</h3>
                <p>{post.excerpt}</p>
                <Link
                  href={`/blog/${post.slug}`}
                  style={{
                    color: "var(--yellow)",
                    marginTop: 16,
                    display: "inline-block",
                    textDecoration: "underline",
                  }}
                >
                  Читать
                </Link>
              </article>
            ))}
          </div>
          <div style={{ marginTop: 40 }}>
            <Button href={site.cta.href}>{site.cta.label}</Button>
          </div>
        </div>
      </section>
    </main>
  );
}
