import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { generateTrip } from '../api/plannerApi'
import { errorMessage } from '../api/client'
import TripForm from '../components/forms/TripForm'
import AgentProgress from '../components/itinerary/AgentProgress'

export default function Planner() {
  const [busy, setBusy] = useState(false); const [progress, setProgress] = useState(0); const [error, setError] = useState(''); const navigate = useNavigate()
  useEffect(() => { if (!busy) return; const timer = setInterval(() => setProgress((value) => Math.min(6, value + 1)), 2200); return () => clearInterval(timer) }, [busy])
  const submit = async (payload) => { setBusy(true); setProgress(0); setError(''); try { const trip = await generateTrip(payload); navigate(`/trips/${trip.id}`) } catch (err) { setError(errorMessage(err)); setBusy(false) } }
  return <section className="planner-page"><div className="container narrow"><div className="page-heading"><span className="eyebrow">Intelligent trip studio</span><h1>Let’s shape your next journey.</h1><p>Give us the essentials. Seven focused agents will research and validate a plan around you.</p></div>{error && <div className="alert error" role="alert">{error}</div>}{busy ? <AgentProgress active={progress} /> : <TripForm onSubmit={submit} disabled={busy} />}</div></section>
}
