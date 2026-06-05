import { useEffect, useState } from 'react';

export default function Memory() {
  const [memory, setMemory] = useState({});
  const [status, setStatus] = useState('Loading');

  useEffect(() => {
    fetch('/api/memory')
      .then((response) => response.json())
      .then((data) => {
        setMemory(data.memory ?? {});
        setStatus('Synced');
      })
      .catch(() => setStatus('Offline'));
  }, []);

  const entries = Object.entries(memory);

  return (
    <section className="panel-stack">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Long-lived context</p>
          <h2>Memory Vault</h2>
        </div>
        <span className="status-pill">{status}</span>
      </div>
      <div className="memory-grid">
        {entries.length ? (
          entries.map(([key, value]) => (
            <article className="memory-card" key={key}>
              <span>{key}</span>
              <p>{typeof value === 'string' ? value : JSON.stringify(value, null, 2)}</p>
            </article>
          ))
        ) : (
          <article className="empty-state">
            <h2>No saved memory yet</h2>
            <p>Important facts from future conversations can be persisted here.</p>
          </article>
        )}
      </div>
    </section>
  );
}
