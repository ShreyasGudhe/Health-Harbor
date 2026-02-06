import React, { useState } from 'react';
import { Activity, AlertTriangle, User, Scale, Moon, HeartPulse } from 'lucide-react';

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
      <div className="glass-panel card border border-teal-500/20 bg-gradient-to-r from-navy-900/80 via-navy-800 to-navy-800/80">
        <div className="flex items-center gap-3 mb-3">
          <Activity className="w-6 h-6 text-teal-400" />
          <div>
            <h2 className="text-xl font-bold text-white">Health Risk Assessment</h2>
            <p className="text-gray-400 text-sm">Enter your vitals to scan for potential health storms ahead.</p>
          </div>
        </div>
        <div className="flex flex-wrap gap-2 text-xs text-gray-500">
          <span className="range-chip">Real-time scoring</span>
          <span className="range-chip">Evidence-based tips</span>
          <span className="range-chip">Zero data stored</span>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="glass-panel card space-y-5 bg-gradient-to-br from-navy-900/70 via-navy-800/70 to-navy-800/60 border border-navy-700/70">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="input-tile">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="icon-pill"><User className="w-5 h-5" /></span>
                <div>
                  <p className="text-sm text-gray-300">Age</p>
                  <p className="text-xs text-gray-500">Years on deck</p>
                </div>
              </div>
              <span className="range-chip">18-80</span>
            </div>
            <input
              type="number"
              className="input-ghost"
              placeholder="25"
              value={form.age}
              onChange={(e) => setForm({ ...form, age: e.target.value })}
              required
            />
          </div>

          <div className="input-tile">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="icon-pill"><Scale className="w-5 h-5" /></span>
                <div>
                  <p className="text-sm text-gray-300">BMI</p>
                  <p className="text-xs text-gray-500">Body balance</p>
                </div>
              </div>
              <span className="range-chip">18.5 - 24.9</span>
            </div>
            <input
              type="number"
              step="0.1"
              className="input-ghost"
              placeholder="22.5"
              value={form.bmi}
              onChange={(e) => setForm({ ...form, bmi: e.target.value })}
              required
            />
          </div>

          <div className="input-tile">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="icon-pill"><Moon className="w-5 h-5" /></span>
                <div>
                  <p className="text-sm text-gray-300">Sleep Hours</p>
                  <p className="text-xs text-gray-500">Last night</p>
                </div>
              </div>
              <span className="range-chip">7-9 hrs</span>
            </div>
            <input
              type="number"
              step="0.5"
              className="input-ghost"
              placeholder="7"
              value={form.sleep_hours}
              onChange={(e) => setForm({ ...form, sleep_hours: e.target.value })}
              required
            />
          </div>

          <div className="input-tile">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="icon-pill"><HeartPulse className="w-5 h-5" /></span>
                <div>
                  <p className="text-sm text-gray-300">Blood Pressure</p>
                  <p className="text-xs text-gray-500">Systolic</p>
                </div>
              </div>
              <span className="range-chip">110-130</span>
            </div>
            <input
              type="number"
              className="input-ghost"
              placeholder="120"
              value={form.blood_pressure}
              onChange={(e) => setForm({ ...form, blood_pressure: e.target.value })}
            />
          </div>
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <p className="text-sm text-gray-500">We crunch these vitals locally to craft a personalized risk radar.</p>
          <button type="submit" className="btn-primary w-full sm:w-auto px-6" disabled={loading}>
            {loading ? 'Scanning...' : '🔍 Scan for Health Storms'}
          </button>
        </div>
      </form>

      {result && (
        <div className={`glass-panel card border ${result.risk_level === 'high' ? 'border-red-500/50' : result.risk_level === 'moderate' ? 'border-yellow-500/50' : 'border-green-500/50'} bg-gradient-to-br from-navy-900/80 to-navy-800/70`}>
          <div className="flex items-center gap-2 mb-3">
            <AlertTriangle className="w-5 h-5 text-yellow-400" />
            <h3 className="font-semibold text-white">Risk Assessment Result</h3>
          </div>
          <div className="flex items-center justify-between mb-3">
            <p className="text-lg text-white">Risk Level: <span className="capitalize font-bold">{result.risk_level}</span></p>
            <span className="range-chip">Score {(result.risk_score * 100).toFixed(0)}%</span>
          </div>
          <div>
            <p className="text-sm text-gray-400 mb-1">Recommendations:</p>
            <ul className="list-disc list-inside text-sm text-gray-200 space-y-1">
              {result.recommendations.map((r, i) => <li key={i}>{r}</li>)}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default StormWatch;
