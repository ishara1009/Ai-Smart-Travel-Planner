export default function BudgetSummary({ budget }) {
  if (!budget) return null
  const percent = Math.min(100, Math.round((budget.estimated_total / budget.total_budget) * 100))
  return <article className="budget-card"><div className="card-heading"><div><span className="eyebrow">Estimated budget</span><h3>{budget.currency} {budget.estimated_total.toLocaleString()}</h3></div><span className={`status-pill ${budget.within_budget ? 'success' : 'danger'}`}>{budget.within_budget ? 'Within budget' : 'Over budget'}</span></div><div className="budget-bar"><span style={{ width: `${percent}%` }} /></div><div className="budget-categories">{budget.categories.map((item) => <div key={item.name}><span>{item.name}</span><strong>{budget.currency} {item.estimated_amount.toLocaleString()}</strong></div>)}</div><small>All costs are planning estimates. Verify prices before booking.</small></article>
}
