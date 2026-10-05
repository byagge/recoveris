import { HeroMark } from "@/components/icons";
import { Button } from "@/components/ui/Button";
import { hero } from "@/content/individuals";
import { site } from "@/content/site";

export function HeroSection() {
  return (
    <section className="main" style={{ paddingBottom: 43 }}>
      <div className="container">
        <div className="main-wrapper">
          <div className="main-content">
            <h1>
              {hero.title} <span>{hero.titleHighlight}</span>
            </h1>
            <h4>{hero.subtitle}</h4>
            {hero.paragraphs.map((p) => (
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
  );
}
