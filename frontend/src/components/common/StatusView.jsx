export function ErrorState({ message, onRetry }) {
  return <div className="state-card error-state"><span>!</span><h3>Something went off route</h3><p>{message}</p>{onRetry && <button className="button secondary" onClick={onRetry}>Try again</button>}</div>
}

export function EmptyState({ title, message, action }) {
  return <div className="state-card"><span className="empty-icon">⌁</span><h3>{title}</h3><p>{message}</p>{action}</div>
}
