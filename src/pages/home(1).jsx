const metrics = [
  { label: 'Agents', value: '6', detail: 'planner, coder, analyst, executor, memory, researcher' },
  { label: 'Memory', value: '5', detail: 'working, short, long, episodic, semantic layers' },
  { label: 'Pipelines', value: '4', detail: 'documents, search, training, embeddings' },
];

export default function Home({ onNavigate }) {
  return (
    <section className="home-grid">
      <div className="hero-band">
        <div>
          <p className="eyebrow">Command center</p>
          <h2>KAYA is your private AI workspace for memory, research, execution, and training.</h2>
          <p>
            Chat with the assistant, curate durable memory, coordinate agents, and prepare local
            datasets from one focused cockpit.
          </p>
          <div className="action-row">
            <button onClick={() => onNavigate('chat')} type="button">Open Chat</button>
            <button className="secondary" onClick={() => onNavigate('memory')} type="button">
              Review Memory
            </button>
          </div>
        </div>
      </div>

      <div className="metric-row">
        {metrics.map((metric) => (
          <article className="metric-card" key={metric.label}>
            <span>{metric.label}</span>
            <strong>{metric.value}</strong>
            <p>{metric.detail}</p>
          </article>
        ))}
      </div>

      <div className="split-grid">
        <section className="panel">
          <h2>Today</h2>
          <ul className="task-list">
            <li><span /> Stabilize API routes and local fallback inference.</li>
            <li><span /> Build a usable workspace shell.</li>
            <li><span /> Keep data directories ready for future RAG and training.</li>
          </ul>
        </section>
        <section className="panel">
          <h2>System Health</h2>
          <div className="health-list">
            <p><strong>Backend</strong><span>FastAPI service</span></p>
            <p><strong>Frontend</strong><span>Vite React app</span></p>
            <p><strong>Storage</strong><span>Local JSON memory</span></p>
          </div>
        </section>
      </div>
    </section>
  );
}
