import { useEffect, useState } from 'react';

export default function Memory() {
  const [memory, setMemory] = useState([]);
  const [facts, setFacts] = useState([]);
  const [status, setStatus] = useState('Loading');

  useEffect(() => {
    fetch('/api/memory')
      .then((response) => response.json())
      .then((data) => {
        setMemory(data.memory ?? []);
        setFacts(data.facts ?? []);
        setStatus('Synced');
      })
      .catch(() => setStatus('Offline'));
  }, []);

  return (
    <section className="panel-stack">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Long-lived context</p>
          <h2>Memory Vault</h2>
        </div>
        <span className="status-pill">{status}</span>
      </div>

      <section className="panel">
        <h2>Learned Facts</h2>
        <div className="memory-grid">
          {facts.length ? (
            facts.slice(-12).reverse().map((item, index) => (
              <article className="memory-card" key={`${item.fact}-${index}`}>
                <span>{item.source ?? 'conversation'}</span>
                <p>{item.fact}</p>
              </article>
            ))
          ) : (
            <article className="empty-state">
              <h2>No durable facts yet</h2>
              <p>Tell KAYA things like "remember that..." or "my name is..." to save them.</p>
            </article>
          )}
        </div>
      </section>

      <section className="panel">
        <h2>Recent Conversations</h2>
        <div className="memory-grid">
          {memory.length ? (
            memory.slice(-12).reverse().map((item, index) => (
              <article className="memory-card" key={`${item.session_id}-${index}`}>
                <span>{item.session_id}</span>
                <p><strong>You:</strong> {item.user}</p>
                <p><strong>KAYA:</strong> {item.assistant}</p>
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
    </section>
  );
}
