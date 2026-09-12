const agents = ['Understanding request', 'Searching attractions', 'Checking weather', 'Analyzing budget', 'Building recommendations', 'Creating itinerary', 'Validating plan']

export default function AgentProgress({ active = 0 }) {
  return <section className="progress-panel" aria-live="polite"><span className="eyebrow light-text">Your planning team is working</span><h2>{agents[Math.min(active, agents.length - 1)]}</h2><div className="progress-track"><span style={{ width: `${((active + 1) / agents.length) * 100}%` }} /></div><div className="agent-dots">{agents.map((label, index) => <div key={label} className={index <= active ? 'active' : ''}><span>{index < active ? '✓' : index + 1}</span><small>{label}</small></div>)}</div><p>We use high-level progress only—your private AI reasoning is never displayed.</p></section>
}
