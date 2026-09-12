import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const signOut = () => { logout(); navigate('/') }
  return <header className="navbar">
    <div className="container nav-inner">
      <Link className="brand" to="/"><span className="brand-mark">A</span><span>Atlas<span className="brand-accent">AI</span></span></Link>
      <nav aria-label="Main navigation">
        <NavLink to="/">Home</NavLink>
        {user && <NavLink to="/planner">Planner</NavLink>}
        {user && <NavLink to="/trips">Saved trips</NavLink>}
      </nav>
      <div className="nav-actions">
        {user ? <><NavLink className="avatar-link" to="/profile" aria-label="Profile">{user.name?.charAt(0).toUpperCase()}</NavLink><button className="text-button" onClick={signOut}>Log out</button></> : <><Link className="text-button" to="/login">Log in</Link><Link className="button small" to="/register">Get started</Link></>}
      </div>
    </div>
  </header>
}
