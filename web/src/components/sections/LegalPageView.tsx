type Section = { heading: string; body: string };

export function LegalPageView({
  title,
  updated,
  sections,
}: {
  title: string;
  updated: string;
  sections: Section[];
}) {
  return (
    <main className="page-template-services">
      <section className="main" style={{ paddingBottom: 80, paddingTop: 160 }}>
        <div className="container" style={{ maxWidth: 900 }}>
          <h1 style={{ marginBottom: 12 }}>{title}</h1>
          <p style={{ marginBottom: 40 }}>Обновлено: {updated}</p>
          {sections.map((s) => (
            <div key={s.heading} style={{ marginBottom: 28 }}>
              <h2 style={{ fontSize: "var(--xl-font-size)", marginBottom: 12 }}>
                {s.heading}
              </h2>
              <p style={{ margin: 0 }}>{s.body}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
