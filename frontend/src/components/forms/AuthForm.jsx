import { useState } from 'react'
import LoadingSpinner from '../common/LoadingSpinner'

export default function AuthForm({ mode, onSubmit, error }) {
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [busy, setBusy] = useState(false)
  const submit = async (event) => {
    event.preventDefault(); setBusy(true)
    try { await onSubmit(mode === 'register' ? form : { email: form.email, password: form.password }) }
    finally { setBusy(false) }
  }
  return <form className="auth-form" onSubmit={submit}>
    {mode === 'register' && <label>Full name<input required minLength="2" maxLength="80" autoComplete="name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></label>}
    <label>Email address<input required type="email" autoComplete="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></label>
    <label>Password<input required type="password" minLength="8" maxLength="128" autoComplete={mode === 'register' ? 'new-password' : 'current-password'} value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></label>
    {error && <p className="form-error" role="alert">{error}</p>}
    <button className="button wide" disabled={busy}>{busy ? <LoadingSpinner label="Please wait" /> : mode === 'register' ? 'Create my account' : 'Log in'}</button>
  </form>
}
