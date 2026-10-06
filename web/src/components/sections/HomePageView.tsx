"use client";

import Link from "next/link";
import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { CtaBgMark, HeroMark } from "@/components/icons";
import { home } from "@/content/pages";
import { site } from "@/content/site";

export function HomePageView() {
  const [openFaq, setOpenFaq] = useState<number | null>(0);

  return (
    <main className="page-template-services">
      <section className="main" style={{ paddingBottom: 43 }}>
        <div className="container">
          <div className="main-wrapper">
            <div className="main-content">
              <h1>
                {home.heroTitle} <span>{home.heroHighlight}</span>
              </h1>
              <h4>{home.heroSubtitle}</h4>
              <p>{home.heroText}</p>
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

      <section className="benefits" id="audiences">
        <div className="container">
          <div className="section-heading">
            <h2>
              Кому <span>помогаем</span>
            </h2>
          </div>
          <div className="services-wrapper" style={{ marginBottom: 20 }}>
            {home.audiences.map((item) => (
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
        </div>
      </section>

      <section className="techniques formats" id="about">
        <div className="container">
          <div className="techniques-heading">
            <h2>
              <span>{home.about.title}</span>
            </h2>
            <p style={{ maxWidth: 536 }}>{home.about.text}</p>
          </div>
        </div>
      </section>

      <section className="benefits" id="casestudies">
        <div className="container">
          <div className="section-heading">
            <h2>
              Кейсы <span>и результаты</span>
            </h2>
          </div>
          <div
            className="services-wrapper"
            style={{
              gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            }}
          >
            {home.cases.map((item) => (
              <div className="services-item" key={item.title}>
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="instructors" id="team">
        <div className="container">
          <div className="instructors-heading">
            <h2>
              Команда <span>Recoveris</span>
            </h2>
            <div className="sub-title">
              Следователи, юристы и инженеры с опытом правоохранения, FIU и
              блокчейн-форензики. Подробнее о ключевых экспертах — на странице
              для частных лиц.
            </div>
          </div>
          <Button href="/individuals">{site.cta.label}</Button>
        </div>
      </section>

      <section className="section-faq" id="faq">
        <div className="container">
          <h2>FAQ</h2>
          <div className="faq-list">
            {home.faq.map((item, index) => (
              <div
                key={item.q}
                className={`faq-item${openFaq === index ? " active" : ""}`}
              >
                <button
                  type="button"
                  className="faq-trigger"
                  onClick={() =>
                    setOpenFaq((cur) => (cur === index ? null : index))
                  }
                >
                  <span>{item.q}</span>
                  <span className="faq-icon">
                    {openFaq === index ? "−" : "+"}
                  </span>
                </button>
                <div className="faq-body">
                  <p>{item.a}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section
        className="section-cta"
        id="contact"
        style={{ paddingTop: 120, paddingBottom: 43 }}
      >
        <div className="container">
          <div className="section-cta-inner">
            <h2>Конфиденциальная консультация</h2>
            <p>
              Расскажите, что произошло — подготовим предварительную оценку
              вариантов.
            </p>
            <Button href="/contact" variant="secondary">
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
