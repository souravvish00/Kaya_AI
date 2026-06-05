import { useState } from 'react';

const metrics = [
  { label: 'Agents', value: '6', detail: 'planner, coder, analyst, executor, memory, researcher' },
  { label: 'Memory', value: '5', detail: 'working, short, long, episodic, semantic layers' },
  { label: 'Pipelines', value: '4', detail: 'documents, search, training, embeddings' },
];

export default function Home({ onNavigate }) {
  const [copyState, setCopyState] = useState('Copy command');
  const launchCommand = 'npm run kaya';

  const copyLaunchCommand = async () => {
    try {
      await navigator.clipboard.writeText(launchCommand);
      setCopyState('Copied');
      window.setTimeout(() => setCopyState('Copy command'), 1800);
    } catch {
      setCopyState(launchCommand);
    }
  };

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

      <section className="launch-panel">
        <div>
          <p className="eyebrow">One code launcher</p>
          <h2>Run frontend, backend, and API together.</h2>
          <p>Use this from the KAYA folder whenever you want the complete local workspace online.</p>
        </div>
        <div className="launch-command">
          <code>{launchCommand}</code>
          <button onClick={copyLaunchCommand} type="button">{copyState}</button>
        </div>
      </section>

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
