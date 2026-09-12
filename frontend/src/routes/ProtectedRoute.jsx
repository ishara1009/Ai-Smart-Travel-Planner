import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import LoadingSpinner from '../components/common/LoadingSpinner'

export default function ProtectedRoute() {
  const { user, loading } = useAuth()
  const location = useLocation()
  if (loading) return <div className="page-center"><LoadingSpinner label="Checking your session" /></div>
  return user ? <Outlet /> : <Navigate to="/login" replace state={{ from: location }} />
}
