"use client";

import { useState } from "react";
import { AccordionArrow } from "@/components/icons";
import { Button } from "@/components/ui/Button";
import { scamTypes } from "@/content/individuals";
import { site } from "@/content/site";

export function ScamTypesSection() {
  const [active, setActive] = useState(0);

  return (
    <section className="levels">
      <div className="container">
        <div className="levels-heading">
          <h2>
            {scamTypes.title} <span>{scamTypes.titleHighlight}</span>
          </h2>
          <div className="sub-title">{scamTypes.subtitle}</div>
        </div>

        <div className="levels-wrapper accordion-container">
          {scamTypes.items.map((item, index) => (
            <div
              key={item.title}
              className={`accordion-section${active === index ? " active" : ""}`}
            >
              <h3
                className="accordion-trigger"
                onClick={() =>
                  setActive((cur) => (cur === index ? -1 : index))
                }
              >
                <span>{item.title}</span>
                <AccordionArrow className="accordion-arrow" />
              </h3>
              <div className="accordion-content">{item.content}</div>
            </div>
          ))}
        </div>

        <div className="alert-block">
          <div className="alert-block-wrapper">
            <h3>{scamTypes.alert.title}</h3>
            <p>{scamTypes.alert.text}</p>
            <Button href={site.cta.href}>{site.cta.label}</Button>
          </div>
        </div>
      </div>
    </section>
  );
}
