import { CtaBgMark } from "@/components/icons";
import { Button } from "@/components/ui/Button";
import { cta } from "@/content/individuals";
import { site } from "@/content/site";

export function CtaSection() {
  return (
    <section
      className="section-cta"
      style={{ paddingTop: 120, paddingBottom: 43 }}
    >
      <div className="container">
        <div className="section-cta-inner">
          <h2 style={{ maxWidth: "85%" }}>{cta.title}</h2>
          <p>{cta.text}</p>
          <Button href={site.cta.href} variant="secondary">
            {site.cta.label}
          </Button>
        </div>
      </div>
      <div className="section-cta-bg">
        <CtaBgMark />
      </div>
    </section>
  );
}
