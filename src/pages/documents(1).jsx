const documentFlows = [
  'Upload source files',
  'Extract clean text',
  'Chunk and embed content',
  'Retrieve context for chat',
];

export default function Documents() {
  return (
    <section className="panel-stack">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Knowledge intake</p>
          <h2>Documents</h2>
        </div>
        <button type="button">Add Source</button>
      </div>
      <div className="timeline">
        {documentFlows.map((flow, index) => (
          <article key={flow}>
            <strong>{String(index + 1).padStart(2, '0')}</strong>
            <p>{flow}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
