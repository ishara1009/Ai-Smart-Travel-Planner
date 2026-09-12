import { Link } from 'react-router-dom'

export default function Footer() {
  return <footer className="footer"><div className="container footer-grid"><div><div className="brand light"><span className="brand-mark">A</span>AtlasAI</div><p>Thoughtful trips, built around the way you travel.</p></div><div><strong>Explore</strong><Link to="/planner">Plan a trip</Link><Link to="/trips">Saved trips</Link></div><div><strong>Built with care</strong><span>Live sources</span><span>Weather-aware</span><span>Budget-conscious</span></div></div><div className="container footer-bottom">© {new Date().getFullYear()} AtlasAI · Verify live details before travel.</div></footer>
}
