import type { Metadata } from "next";
import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { knowledgeCenter } from "@/content/pages";
import { site } from "@/content/site";

export const metadata: Metadata = {
  title: knowledgeCenter.title,
  description: knowledgeCenter.subtitle,
};

export default function KnowledgeCenterPage() {
  return (
    <main className="page-template-services">
      <section className="main" style={{ paddingBottom: 80 }}>
        <div className="container">
          <h1 style={{ marginBottom: 16 }}>
            База <span>знаний</span>
          </h1>
          <p style={{ marginBottom: 48, maxWidth: 640 }}>
            {knowledgeCenter.subtitle}
          </p>
          <div
            className="services-wrapper"
            style={{
              gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
              marginTop: 0,
            }}
          >
            {knowledgeCenter.items.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="services-item"
                style={{ textDecoration: "none" }}
              >
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </Link>
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
