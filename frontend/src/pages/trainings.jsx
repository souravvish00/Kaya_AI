import { useEffect, useState } from 'react';

const apiFetch = async (path, options) => {
  try {
    return await fetch(path, options);
  } catch (proxyError) {
    return fetch(`http://127.0.0.1:8000${path}`, options);
  }
};

export default function Trainings() {
  const [status, setStatus] = useState({ stats: {}, jobs: [] });
  const [examples, setExamples] = useState([]);
  const [form, setForm] = useState({
    prompt: '',
    completion: '',
    tags: 'manual',
    rating: 5,
  });
  const [job, setJob] = useState({
    model_name: 'Qwen/Qwen3-8B',
    method: 'lora',
    epochs: 3,
    learning_rate: 0.0002,
  });
  const [notice, setNotice] = useState('');

  const refresh = async () => {
    const [statusResponse, examplesResponse] = await Promise.all([
      apiFetch('/api/training/status'),
      apiFetch('/api/training/examples'),
    ]);
    setStatus(await statusResponse.json());
    setExamples((await examplesResponse.json()).examples ?? []);
  };

  useEffect(() => {
    refresh().catch(() => setNotice('Training API is offline.'));
  }, []);

  const saveExample = async (event) => {
    event.preventDefault();
    const payload = {
      prompt: form.prompt,
      completion: form.completion,
      tags: form.tags.split(',').map((tag) => tag.trim()).filter(Boolean),
      rating: Number(form.rating),
    };
    const response = await apiFetch('/api/training/examples', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    setNotice(response.ok ? 'Training example saved.' : 'Could not save example.');
    setForm({ prompt: '', completion: '', tags: 'manual', rating: 5 });
    refresh();
  };

  const exportDataset = async () => {
    const response = await apiFetch('/api/training/export', { method: 'POST' });
    const data = await response.json();
    setNotice(`Exported ${data.examples} examples to ${data.path}`);
    refresh();
  };

  const seedMath = async () => {
    const response = await apiFetch('/api/training/seed/math-grade-12', { method: 'POST' });
    const data = await response.json();
    setNotice(response.ok ? `Added ${data.examples} grade-12 math examples.` : 'Could not add math examples.');
    refresh();
  };

  const configureJob = async (event) => {
    event.preventDefault();
    const response = await apiFetch('/api/training/jobs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...job,
        epochs: Number(job.epochs),
        learning_rate: Number(job.learning_rate),
      }),
    });
    const data = await response.json();
    setNotice(response.ok ? `Training job configured: ${data.job.command}` : 'Could not configure job.');
    refresh();
  };

  return (
    <section className="panel-stack">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Model improvement</p>
          <h2>Training Lab</h2>
        </div>
        <div className="action-row compact-actions">
          <button className="secondary" onClick={seedMath} type="button">Add 12th math</button>
          <button onClick={exportDataset} type="button">Export JSONL</button>
        </div>
      </div>

      <div className="training-board">
        <article>
          <h3>Examples</h3>
          <strong>{status.stats?.examples ?? 0}</strong>
          <p>Total prompt and ideal reply pairs.</p>
          <progress max="100" value={Math.min(status.stats?.examples ?? 0, 100)} />
        </article>
        <article>
          <h3>High quality</h3>
          <strong>{status.stats?.high_quality ?? 0}</strong>
          <p>Rated 4 or 5. Aim for 20 before the first fine-tune.</p>
          <progress max="20" value={Math.min(status.stats?.high_quality ?? 0, 20)} />
        </article>
        <article>
          <h3>Fine-tune ready</h3>
          <strong>{status.stats?.ready_for_finetune ? 'Yes' : 'Not yet'}</strong>
          <p>Export a dataset before launching training.</p>
          <progress max="1" value={status.stats?.ready_for_finetune ? 1 : 0} />
        </article>
      </div>

      <div className="training-workspace">
        <form className="trainer-form" onSubmit={saveExample}>
          <h3>Add ideal reply</h3>
          <textarea
            onChange={(event) => setForm({ ...form, prompt: event.target.value })}
            placeholder="User prompt"
            required
            value={form.prompt}
          />
          <textarea
            onChange={(event) => setForm({ ...form, completion: event.target.value })}
            placeholder="Perfect assistant reply"
            required
            value={form.completion}
          />
          <div className="form-row">
            <input
              onChange={(event) => setForm({ ...form, tags: event.target.value })}
              placeholder="tags"
              value={form.tags}
            />
            <input
              max="5"
              min="1"
              onChange={(event) => setForm({ ...form, rating: event.target.value })}
              type="number"
              value={form.rating}
            />
          </div>
          <button type="submit">Save example</button>
        </form>

        <form className="trainer-form" onSubmit={configureJob}>
          <h3>Configure LLM training</h3>
          <input
            onChange={(event) => setJob({ ...job, model_name: event.target.value })}
            value={job.model_name}
          />
          <div className="form-row">
            <select onChange={(event) => setJob({ ...job, method: event.target.value })} value={job.method}>
              <option value="lora">LoRA</option>
              <option value="qlora">QLoRA</option>
              <option value="full">Full fine-tune</option>
            </select>
            <input
              min="1"
              onChange={(event) => setJob({ ...job, epochs: event.target.value })}
              type="number"
              value={job.epochs}
            />
          </div>
          <input
            onChange={(event) => setJob({ ...job, learning_rate: event.target.value })}
            step="0.0001"
            type="number"
            value={job.learning_rate}
          />
          <button type="submit">Create training job</button>
        </form>
      </div>

      {notice ? <p className="inline-notice">{notice}</p> : null}

      <section className="panel">
        <h2>Latest Examples</h2>
        <div className="example-list">
          {examples.length ? (
            examples.slice(-6).reverse().map((example) => (
              <article key={example.id}>
                <strong>{example.prompt}</strong>
                <p>{example.completion ?? example.response}</p>
                <span>Rating {example.rating} - {(example.tags ?? []).join(', ')}</span>
              </article>
            ))
          ) : (
            <p>No examples yet. Save replies from Chat or add ideal replies here.</p>
          )}
        </div>
      </section>
    </section>
  );
}
