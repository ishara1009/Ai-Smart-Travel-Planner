export default function RecommendationCard({ item }) {
  return <article className="recommendation-card"><span className="category">{item.category}</span><h3>{item.name}</h3><p>{item.reason}</p><div>{item.estimated_cost != null && <span>Est. {item.estimated_cost.toLocaleString()}</span>}{item.source_url && <a href={item.source_url} target="_blank" rel="noreferrer">View source ↗</a>}</div></article>
}
