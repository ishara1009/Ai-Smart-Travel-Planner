import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { login } from '../api/authApi'
import { errorMessage } from '../api/client'
import AuthForm from '../components/forms/AuthForm'
import { useAuth } from '../hooks/useAuth'

export default function Login() {
  const [error, setError] = useState(''); const { completeAuth } = useAuth(); const navigate = useNavigate(); const location = useLocation()
  const submit = async (payload) => { setError(''); try { completeAuth(await login(payload)); navigate(location.state?.from?.pathname || '/planner', { replace: true }) } catch (err) { setError(errorMessage(err)) } }
  return <section className="auth-page"><div className="auth-aside"><span className="eyebrow light-text">Welcome back</span><h1>Your next route is waiting.</h1><p>Return to saved trips, refine a plan, or begin somewhere completely new.</p><blockquote>“A journey is best measured in friends, rather than miles.”<small>— Tim Cahill</small></blockquote></div><div className="auth-panel"><div className="auth-card"><span className="eyebrow">Account access</span><h2>Log in to AtlasAI</h2><p>New here? <Link to="/register">Create an account</Link></p><AuthForm mode="login" onSubmit={submit} error={error} /></div></div></section>
}
