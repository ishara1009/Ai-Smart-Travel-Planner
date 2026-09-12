import { Route, Routes } from 'react-router-dom'
import AppLayout from './layouts/AppLayout'
import ProtectedRoute from './routes/ProtectedRoute'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Planner from './pages/Planner'
import TripDetails from './pages/TripDetails'
import SavedTrips from './pages/SavedTrips'
import Profile from './pages/Profile'

export default function App() {
  return <Routes><Route element={<AppLayout />}><Route index element={<Home />} /><Route path="login" element={<Login />} /><Route path="register" element={<Register />} /><Route element={<ProtectedRoute />}><Route path="planner" element={<Planner />} /><Route path="trips" element={<SavedTrips />} /><Route path="trips/:tripId" element={<TripDetails />} /><Route path="profile" element={<Profile />} /></Route><Route path="*" element={<Home />} /></Route></Routes>
}
