import { Button } from "@/components/ui/Button";
import { CtaBgMark, HeroMark } from "@/components/icons";
import type { MarketingPage } from "@/content/pages";
import { site } from "@/content/site";

export function MarketingPageView({ page }: { page: MarketingPage }) {
  return (
    <main className="page-template-services">
      <section className="main" style={{ paddingBottom: 43 }}>
        <div className="container">
          <div className="main-wrapper">
            <div className="main-content">
              <h1>
                {page.heroTitle}{" "}
                {page.heroHighlight ? <span>{page.heroHighlight}</span> : null}
              </h1>
              <p>{page.heroSubtitle}</p>
              {page.paragraphs?.map((p) => (
                <p key={p}>{p}</p>
              ))}
              <div className="main-buttons">
                <Button href={site.cta.href}>{site.cta.label}</Button>
              </div>
            </div>
            <div className="main-details">
              <HeroMark />
            </div>
          </div>
        </div>
      </section>

      {page.sections.map((section) => (
        <section className="benefits" key={section.title}>
          <div className="container">
            <div className="section-heading">
              <h2>
                {section.title}{" "}
                {section.titleHighlight ? (
                  <span>{section.titleHighlight}</span>
                ) : null}
              </h2>
              {section.subtitle ? (
                <div className="sub-title">{section.subtitle}</div>
              ) : null}
            </div>
            <div
              className="services-wrapper"
              style={{
                marginBottom: 50,
                gridTemplateColumns:
                  section.items.length >= 4
                    ? "repeat(auto-fit, minmax(260px, 1fr))"
                    : undefined,
              }}
            >
              {section.items.map((item) => (
                <div className="services-item" key={item.title}>
                  <h3>{item.title}</h3>
                  <p>{item.description}</p>
                </div>
              ))}
            </div>
            <Button href={site.cta.href}>{site.cta.label}</Button>
          </div>
        </section>
      ))}

      <section
        className="section-cta"
        style={{ paddingTop: 120, paddingBottom: 43 }}
      >
        <div className="container">
          <div className="section-cta-inner">
            <h2 style={{ maxWidth: "85%" }}>
              {page.ctaTitle ?? "Свяжитесь с нами"}
            </h2>
            <p>
              {page.ctaText ??
                "Расскажите о ситуации — дадим предварительную оценку конфиденциально."}
            </p>
            <Button href={site.cta.href} variant="secondary">
              {site.cta.label}
            </Button>
          </div>
        </div>
        <div className="section-cta-bg">
          <CtaBgMark />
        </div>
      </section>
    </main>
  );
}
