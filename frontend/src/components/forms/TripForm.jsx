import { useState } from 'react'

const interestOptions = ['Nature', 'Culture', 'Food', 'Adventure', 'History', 'Wellness']
const transportOptions = ['Train', 'Walking', 'Public bus', 'Rental car', 'Taxi']

export default function TripForm({ onSubmit, disabled }) {
  const tomorrow = new Date(Date.now() + 86400000).toISOString().slice(0, 10)
  const [form, setForm] = useState({ destination: '', start_date: tomorrow, days: 3, travelers: 2, budget: 60000, currency: 'LKR', interests: ['Nature', 'Culture'], transport_preferences: ['Train'], accommodation_preference: 'Mid-range hotel', food_preference: '', activity_preferences: [], special_requirements: '' })
  const toggle = (field, option) => setForm((current) => ({ ...current, [field]: current[field].includes(option) ? current[field].filter((item) => item !== option) : [...current[field], option] }))
  const submit = (event) => { event.preventDefault(); onSubmit({ ...form, days: Number(form.days), travelers: Number(form.travelers), budget: Number(form.budget) }) }
  return <form className="trip-form" onSubmit={submit}>
    <div className="form-section"><div><span className="step-kicker">01 · Essentials</span><h2>Where are you heading?</h2></div><div className="form-grid">
      <label className="span-2">Destination<input required minLength="2" maxLength="120" placeholder="e.g. Kandy, Sri Lanka" value={form.destination} onChange={(e) => setForm({ ...form, destination: e.target.value })} /></label>
      <label>Start date<input required type="date" min={tomorrow} value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} /></label>
      <label>Trip length<input required type="number" min="1" max="30" value={form.days} onChange={(e) => setForm({ ...form, days: e.target.value })} /><small>days</small></label>
      <label>Travelers<input required type="number" min="1" max="50" value={form.travelers} onChange={(e) => setForm({ ...form, travelers: e.target.value })} /></label>
      <label>Budget<div className="input-pair"><input required type="number" min="1" value={form.budget} onChange={(e) => setForm({ ...form, budget: e.target.value })} /><select value={form.currency} onChange={(e) => setForm({ ...form, currency: e.target.value })}><option>LKR</option><option>USD</option><option>EUR</option><option>GBP</option><option>INR</option></select></div></label>
    </div></div>
    <div className="form-section"><div><span className="step-kicker">02 · Your style</span><h2>What makes a trip yours?</h2></div>
      <fieldset><legend>Interests</legend><div className="chip-group">{interestOptions.map((item) => <button type="button" key={item} className={`choice-chip ${form.interests.includes(item) ? 'selected' : ''}`} onClick={() => toggle('interests', item)}>{item}</button>)}</div></fieldset>
      <fieldset><legend>Preferred transport</legend><div className="chip-group">{transportOptions.map((item) => <button type="button" key={item} className={`choice-chip ${form.transport_preferences.includes(item) ? 'selected' : ''}`} onClick={() => toggle('transport_preferences', item)}>{item}</button>)}</div></fieldset>
      <div className="form-grid"><label>Accommodation<select value={form.accommodation_preference} onChange={(e) => setForm({ ...form, accommodation_preference: e.target.value })}><option>Budget guesthouse</option><option>Mid-range hotel</option><option>Boutique hotel</option><option>Luxury hotel</option><option>Hostel</option></select></label><label>Food preference<input maxLength="100" placeholder="Vegetarian, local food…" value={form.food_preference} onChange={(e) => setForm({ ...form, food_preference: e.target.value })} /></label><label className="span-2">Notes or special requirements<textarea maxLength="1000" rows="4" placeholder="Accessibility, pace, dietary needs…" value={form.special_requirements} onChange={(e) => setForm({ ...form, special_requirements: e.target.value })} /></label></div>
    </div>
    <button className="button planner-submit" disabled={disabled}>{disabled ? 'Building your trip…' : 'Create my intelligent itinerary'} <span>→</span></button>
  </form>
}
