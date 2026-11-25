import { useEffect, useState } from 'react';
import { apiRequest } from '../api/client.js';

const initial = { patient_name: '', appointment_type: 'General Consultation', appointment_time: '', notes: '' };

export function BookingPage() {
  const [form, setForm] = useState(initial);
  const [appointments, setAppointments] = useState([]);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);

  async function load() {
    const data = await apiRequest('/appointments');
    setAppointments(data);
  }

  useEffect(() => { load().catch((e) => setStatus(e.message)); }, []);

  async function submit(e) {
    e.preventDefault();
    setLoading(true); setStatus('');
    try {
      await apiRequest('/appointments', { method: 'POST', body: JSON.stringify(form) });
      setForm(initial);
      setStatus('Appointment booked and saved to SQLite.');
      await load();
    } catch (err) { setStatus(err.message); }
    finally { setLoading(false); }
  }

  return (
    <section className="placeholder-view">
      <div className="placeholder-heading">
        <p>Patient workflow</p>
        <h2>Book Appointment</h2>
        <span>Frontend ↔ FastAPI ↔ SQLite</span>
      </div>
      <form className="form-grid" onSubmit={submit}>
        <label>Patient name<input value={form.patient_name} onChange={e=>setForm({...form, patient_name:e.target.value})} required /></label>
        <label>Appointment type<select value={form.appointment_type} onChange={e=>setForm({...form, appointment_type:e.target.value})}><option>General Consultation</option><option>Dental Checkup</option><option>Follow-up</option></select></label>
        <label>Date & time<input type="datetime-local" value={form.appointment_time} onChange={e=>setForm({...form, appointment_time:e.target.value})} required /></label>
        <label>Notes<input value={form.notes} onChange={e=>setForm({...form, notes:e.target.value})} placeholder="Optional" /></label>
        <button className="primary-btn" disabled={loading} type="submit">{loading ? 'Saving...' : 'Book appointment'}</button>
      </form>
      {status && <p className="status-msg">{status}</p>}
      <div className="list">
        <h3>Recent appointments</h3>
        {appointments.length === 0 ? <p className="placeholder-description">No appointments yet.</p> : appointments.map(a => (
          <article key={a.id} className="workflow-step"><strong>#{a.id}</strong><span>{a.patient_name} — {a.appointment_type} — {a.appointment_time} <em>({a.status})</em></span></article>
        ))}
      </div>
    </section>
  );
}
