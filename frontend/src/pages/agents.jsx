const agents = [
  ['Planner', 'Breaks goals into executable steps.'],
  ['Researcher', 'Collects and compares source material.'],
  ['Coder', 'Implements product and automation work.'],
  ['Analyst', 'Turns raw data into decisions.'],
  ['Executor', 'Runs tools and coordinates workflows.'],
  ['Memory', 'Extracts durable preferences and facts.'],
];

export default function Agents() {
  return (
    <section className="panel-stack">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Specialists</p>
          <h2>Agent Roster</h2>
        </div>
      </div>
      <div className="card-grid">
        {agents.map(([name, description]) => (
          <article className="agent-card" key={name}>
            <span>{name.slice(0, 1)}</span>
            <h3>{name}</h3>
            <p>{description}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
