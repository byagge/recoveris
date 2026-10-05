import { StepIcon } from "@/components/icons";
import { Button } from "@/components/ui/Button";
import { steps } from "@/content/individuals";
import { site } from "@/content/site";

export function StepsSection() {
  return (
    <section className="benefits">
      <div className="container">
        <div className="section-heading">
          <h2>
            <span>{steps.title}</span> {steps.titleRest}
          </h2>
          <div className="sub-title">{steps.subtitle}</div>
        </div>

        <div className="services-wrapper" style={{ marginBottom: 50 }}>
          {steps.items.map((item) => (
            <div className="services-item" key={item.title}>
              <div className="services-icon">
                <StepIcon type={item.icon} />
              </div>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </div>
          ))}
        </div>

        <Button href={site.cta.href}>{site.cta.label}</Button>
      </div>
    </section>
  );
}
