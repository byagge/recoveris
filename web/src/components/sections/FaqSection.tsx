"use client";

import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { faq } from "@/content/individuals";
import { site } from "@/content/site";

export function FaqSection() {
  const [open, setOpen] = useState<number | null>(null);

  return (
    <section className="section-faq">
      <div className="container">
        <h2>{faq.title}</h2>

        <div className="section-faq-wrapper">
          <div className="faq-list">
            {faq.items.map((item, index) => (
              <div
                key={item.question}
                className={`faq-item${open === index ? " active" : ""}`}
              >
                <button
                  type="button"
                  className="faq-trigger"
                  onClick={() =>
                    setOpen((cur) => (cur === index ? null : index))
                  }
                  aria-expanded={open === index}
                >
                  <span>{item.question}</span>
                  <span className="faq-icon" aria-hidden>
                    {open === index ? "−" : "+"}
                  </span>
                </button>
                <div className="faq-body">
                  <p>{item.answer}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <Button href={site.cta.href}>{site.cta.label}</Button>
      </div>
    </section>
  );
}
