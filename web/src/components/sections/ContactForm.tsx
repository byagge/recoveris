"use client";

import { FormEvent, useState } from "react";
import { site } from "@/content/site";

export function ContactForm() {
  const [sent, setSent] = useState(false);

  function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setSent(true);
  }

  return (
    <main className="page-template-services">
      <section className="main" style={{ paddingBottom: 80 }}>
        <div className="container">
          <div className="main-wrapper" style={{ gridTemplateColumns: "1fr 1fr" }}>
            <div className="main-content">
              <h1>
                Связаться <span>с нами</span>
              </h1>
              <p>
                Опишите ситуацию и детали транзакций. Мы свяжемся для
                предварительной оценки. Не присылайте seed-фразу и не давайте
                удалённый доступ.
              </p>
              <p style={{ marginTop: 20 }}>
                Email:{" "}
                <a href={`mailto:${site.email}`} style={{ color: "var(--yellow)" }}>
                  {site.email}
                </a>
              </p>
              <p>
                {site.legalName}
                <br />
                {site.address.street}
                <br />
                {site.address.city}
                <br />
                {site.address.country}
              </p>
            </div>

            <div
              style={{
                background: "var(--black)",
                borderRadius: "var(--rounded-sm)",
                padding: "40px 32px",
              }}
            >
              {sent ? (
                <p style={{ color: "var(--yellow)", margin: 0 }}>
                  Спасибо! Сообщение принято. Мы свяжемся с вами.
                </p>
              ) : (
                <form className="wpcf7" onSubmit={onSubmit}>
                  <label>
                    Имя
                    <input name="name" type="text" required placeholder="Ваше имя" />
                  </label>
                  <label>
                    Email
                    <input
                      name="email"
                      type="email"
                      required
                      placeholder="you@example.com"
                    />
                  </label>
                  <label>
                    Сообщение
                    <textarea
                      name="message"
                      required
                      rows={5}
                      placeholder="Что произошло, хеши транзакций, сумма..."
                    />
                  </label>
                  <button type="submit" className="btn btn--primary">
                    Отправить
                  </button>
                </form>
              )}
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
