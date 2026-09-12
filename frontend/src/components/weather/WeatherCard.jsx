export default function WeatherCard({ weather }) {
  if (!weather?.available) return <article className="summary-card"><span className="card-icon">◌</span><div><span className="eyebrow">Weather</span><h3>Forecast unavailable</h3><p>{weather?.limitation || 'Check conditions closer to departure.'}</p></div></article>
  return <article className="summary-card"><span className="card-icon">☼</span><div><span className="eyebrow">Current weather</span><h3>{weather.temperature_c}°C · {weather.condition}</h3><p>{weather.location} · Humidity {weather.humidity}% · Wind {weather.wind_kph} km/h</p><small>{weather.limitation}</small></div></article>
}
