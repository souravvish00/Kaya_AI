import { useEffect, useState } from 'react';

const documentFlows = [
  'Upload books or source files',
  'Extract clean text',
  'Chunk content for retrieval',
  'Use sources in chat replies',
];

const apiFetch = async (path, options) => {
  try {
    return await fetch(path, options);
  } catch {
    return fetch(`http://127.0.0.1:8000${path}`, options);
  }
};

export default function Documents() {
  const [documents, setDocuments] = useState([]);
  const [title, setTitle] = useState('Manual knowledge');
  const [text, setText] = useState('');
  const [file, setFile] = useState(null);
  const [notice, setNotice] = useState('');

  const refresh = async () => {
    const response = await apiFetch('/api/documents');
    const data = await response.json();
    setDocuments(data.documents ?? []);
  };

  useEffect(() => {
    refresh().catch(() => setNotice('Document API is offline.'));
  }, []);

  const uploadFile = async (event) => {
    event.preventDefault();
    if (!file) return;

    const body = new FormData();
    body.append('file', file);

    const response = await apiFetch('/api/documents/upload', {
      method: 'POST',
      body,
    });
    const data = await response.json();
    setNotice(response.ok ? `Added ${data.document.title}` : data.detail ?? 'Could not read file.');
    setFile(null);
    refresh();
  };

  const saveText = async (event) => {
    event.preventDefault();
    const body = new FormData();
    body.append('title', title);
    body.append('text', text);

    const response = await apiFetch('/api/documents/text', {
      method: 'POST',
      body,
    });
    const data = await response.json();
    setNotice(response.ok ? `Added ${data.document.title}` : data.detail ?? 'Could not save text.');
    setText('');
    refresh();
  };

  return (
    <section className="panel-stack">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Knowledge intake</p>
          <h2>Documents</h2>
        </div>
      </div>

      <div className="timeline">
        {documentFlows.map((flow, index) => (
          <article key={flow}>
            <strong>{String(index + 1).padStart(2, '0')}</strong>
            <p>{flow}</p>
          </article>
        ))}
      </div>

      <div className="training-workspace">
        <form className="trainer-form" onSubmit={uploadFile}>
          <h3>Add book or file</h3>
          <input
            accept=".txt,.md,.csv,.json,.pdf"
            onChange={(event) => setFile(event.target.files?.[0] ?? null)}
            type="file"
          />
          <button disabled={!file} type="submit">Upload source</button>
        </form>

        <form className="trainer-form" onSubmit={saveText}>
          <h3>Paste knowledge</h3>
          <input
            onChange={(event) => setTitle(event.target.value)}
            placeholder="Source title"
            value={title}
          />
          <textarea
            onChange={(event) => setText(event.target.value)}
            placeholder="Paste book notes, facts, lessons, or training data..."
            required
            value={text}
          />
          <button disabled={!text.trim()} type="submit">Save knowledge</button>
        </form>
      </div>

      {notice ? <p className="inline-notice">{notice}</p> : null}

      <section className="panel">
        <h2>Knowledge Library</h2>
        <div className="example-list">
          {documents.length ? (
            documents.slice().reverse().map((document) => (
              <article key={document.id}>
                <strong>{document.title}</strong>
                <p>{document.chunks} chunks from {document.characters} characters.</p>
                <span>{document.source}</span>
              </article>
            ))
          ) : (
            <p>No sources yet. Upload books or paste data, then ask questions in Chat.</p>
          )}
        </div>
      </section>
    </section>
  );
}
