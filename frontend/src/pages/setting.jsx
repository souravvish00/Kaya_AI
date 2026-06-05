export default function Settings() {
  return (
    <section className="settings-grid">
      <article className="panel">
        <h2>Runtime</h2>
        <label>
          <span>Local-only mode</span>
          <input checked readOnly type="checkbox" />
        </label>
        <label>
          <span>Persist memory</span>
          <input checked readOnly type="checkbox" />
        </label>
      </article>
      <article className="panel">
        <h2>Endpoints</h2>
        <p><strong>API</strong><span>http://localhost:8000</span></p>
        <p><strong>App</strong><span>http://localhost:5173</span></p>
      </article>
    </section>
  );
}
