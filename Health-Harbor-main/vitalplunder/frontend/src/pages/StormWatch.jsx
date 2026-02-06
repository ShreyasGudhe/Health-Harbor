import React, { useState } from 'react';
import { Activity, AlertTriangle } from 'lucide-react';

function StormWatch() {
  const [form, setForm] = useState({ age: '', bmi: '', sleep_hours: '', blood_pressure: '', heart_rate: '' });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    // TODO: API call to /api/storm-watch/predict
    // const response = await api.stormWatch.predict(form);
    setTimeout(() => {
      setResult({ risk_level: 'moderate', risk_score: 0.42, recommendations: ['Monitor blood pressure', 'Improve sleep'] });
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <div className="card">
        <div className="flex items-center gap-3 mb-4">
          <Activity className="w-6 h-6 text-red-400" />
          <h2 className="text-xl font-bold text-white">Health Risk Assessment</h2>
        </div>
        <p className="text-gray-400 text-sm">Enter your vitals to scan for potential health storms on the horizon.</p>
      </div>

      <form onSubmit={handleSubmit} className="card space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm text-gray-400 mb-1">Age</label>
            <input type="number" className="input-field" placeholder="25" value={form.age} onChange={(e) => setForm({...form, age: e.target.value})} required />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">BMI</label>
            <input type="number" step="0.1" className="input-field" placeholder="22.5" value={form.bmi} onChange={(e) => setForm({...form, bmi: e.target.value})} required />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Sleep Hours</label>
            <input type="number" step="0.5" className="input-field" placeholder="7" value={form.sleep_hours} onChange={(e) => setForm({...form, sleep_hours: e.target.value})} required />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Blood Pressure (systolic)</label>
            <input type="number" className="input-field" placeholder="120" value={form.blood_pressure} onChange={(e) => setForm({...form, blood_pressure: e.target.value})} />
          </div>
        </div>
        <button type="submit" className="btn-primary w-full" disabled={loading}>
          {loading ? 'Scanning...' : '🔍 Scan for Health Storms'}
        </button>
      </form>

      {result && (
        <div className={`card border-l-4 ${result.risk_level === 'high' ? 'border-red-500' : result.risk_level === 'moderate' ? 'border-yellow-500' : 'border-green-500'}`}>
          <div className="flex items-center gap-2 mb-3">
            <AlertTriangle className="w-5 h-5 text-yellow-400" />
            <h3 className="font-semibold text-white">Risk Assessment Result</h3>
          </div>
          <p className="text-lg text-white mb-2">Risk Level: <span className="capitalize font-bold">{result.risk_level}</span></p>
          <p className="text-sm text-gray-400 mb-3">Score: {(result.risk_score * 100).toFixed(0)}%</p>
          <div>
            <p className="text-sm text-gray-400 mb-1">Recommendations:</p>
            <ul className="list-disc list-inside text-sm text-gray-300">
              {result.recommendations.map((r, i) => <li key={i}>{r}</li>)}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default StormWatch;
