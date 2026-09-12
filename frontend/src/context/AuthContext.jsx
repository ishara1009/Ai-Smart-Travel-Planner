import { createContext, useCallback, useEffect, useMemo, useState } from 'react'
import { getCurrentUser } from '../api/authApi'

export const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem('travel_user')) }
    catch { return null }
  })
  const [loading, setLoading] = useState(Boolean(localStorage.getItem('travel_token')))

  const logout = useCallback(() => {
    localStorage.removeItem('travel_token')
    localStorage.removeItem('travel_user')
    setUser(null)
    setLoading(false)
  }, [])

  const completeAuth = useCallback((result) => {
    localStorage.setItem('travel_token', result.access_token)
    localStorage.setItem('travel_user', JSON.stringify(result.user))
    setUser(result.user)
  }, [])

  useEffect(() => {
    const onExpired = () => logout()
    window.addEventListener('auth:expired', onExpired)
    if (localStorage.getItem('travel_token')) {
      getCurrentUser().then((value) => {
        setUser(value)
        localStorage.setItem('travel_user', JSON.stringify(value))
      }).catch(logout).finally(() => setLoading(false))
    }
    return () => window.removeEventListener('auth:expired', onExpired)
  }, [logout])

  const value = useMemo(() => ({ user, setUser, loading, completeAuth, logout }), [user, loading, completeAuth, logout])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
