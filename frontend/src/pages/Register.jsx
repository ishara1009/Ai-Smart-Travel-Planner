import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { register } from '../api/authApi'
import { errorMessage } from '../api/client'
import AuthForm from '../components/forms/AuthForm'
import { useAuth } from '../hooks/useAuth'

export default function Register() {
  const [error, setError] = useState(''); const { completeAuth } = useAuth(); const navigate = useNavigate()
  const submit = async (payload) => { setError(''); try { completeAuth(await register(payload)); navigate('/planner') } catch (err) { setError(errorMessage(err)) } }
  return <section className="auth-page"><div className="auth-aside register-aside"><span className="eyebrow light-text">Plan with confidence</span><h1>Less tab-hopping. More looking forward.</h1><p>Your account keeps drafts, approved routes, preferences and every useful source together.</p><div className="aside-points"><span>✓ Private, protected trip library</span><span>✓ Approve, modify or regenerate</span><span>✓ No API keys in the browser</span></div></div><div className="auth-panel"><div className="auth-card"><span className="eyebrow">Begin your journey</span><h2>Create an account</h2><p>Already planning with us? <Link to="/login">Log in</Link></p><AuthForm mode="register" onSubmit={submit} error={error} /></div></div></section>
}
