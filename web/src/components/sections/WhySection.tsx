import { ShieldWarningIcon, WhyIcon } from "@/components/icons";
import { Button } from "@/components/ui/Button";
import { whyRecoveris } from "@/content/individuals";
import { site } from "@/content/site";

export function WhySection() {
  return (
    <section className="techniques formats">
      <div className="container">
        <div className="techniques-heading">
          <h2>
            {whyRecoveris.title} <span>{whyRecoveris.titleHighlight}</span>
          </h2>
        </div>

        <div className="techniques-wrapper">
          {whyRecoveris.items.map((item) => (
            <div className="techniques-item" key={item.title}>
              <WhyIcon type={item.icon} />
              <div>
                <h3>{item.title}</h3>
                <p>{item.description}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="alert-block">
          <div className="alert-block-wrapper">
            <h3>
              <ShieldWarningIcon />
              {whyRecoveris.warning.title}
            </h3>
            <p>
              {whyRecoveris.warning.text}{" "}
              <a
                href={whyRecoveris.warning.linkHref}
                className="text-link"
              >
                [<span>{whyRecoveris.warning.linkLabel}</span>]
              </a>
            </p>
          </div>
          <Button href={site.cta.href}>{site.cta.label}</Button>
        </div>
      </div>
    </section>
  );
}
