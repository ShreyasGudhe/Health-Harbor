import React, { useState } from 'react';
import { Compass, TrendingUp, Dumbbell, Monitor, Footprints, Droplets } from 'lucide-react';

function CaptainsOrders() {
  const [form, setForm] = useState({ exercise_minutes: '', screen_time: '', daily_steps: '', water_intake: '' });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    // TODO: API call to /api/captains-orders/analyze
    // const response = await api.captainsOrders.analyze(form);
    setTimeout(() => {
      setResult({
        lifestyle_score: 72,
        cluster: 'active',
        recommendations: [
          'Great exercise routine! Keep it up.',
          'Consider reducing screen time by 30 minutes.',
          'Try to increase water intake to 8 glasses.'
        ]
      });
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <div className="glass-panel card bg-gradient-to-r from-navy-900/80 via-navy-800/80 to-navy-800/60 border border-blue-500/20">
        <div className="flex items-center gap-3 mb-3">
          <Compass className="w-6 h-6 text-blue-400" />
          <div>
            <h2 className="text-xl font-bold text-white">Lifestyle Coaching</h2>
            <p className="text-gray-400 text-sm">Log your daily habits and get tailored captain's orders.</p>
          </div>
        </div>
        <div className="flex gap-2 text-xs text-gray-500 flex-wrap">
          <span className="range-chip">Personalized score</span>
          <span className="range-chip">Actionable tips</span>
          <span className="range-chip">No data stored</span>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="glass-panel card space-y-5 bg-gradient-to-br from-navy-900/70 via-navy-800/70 to-navy-800/60 border border-navy-700/70">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="input-tile">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="icon-pill"><Dumbbell className="w-5 h-5" /></span>
                <div>
                  <p className="text-sm text-gray-300">Exercise</p>
                  <p className="text-xs text-gray-500">Minutes today</p>
                </div>
              </div>
              <span className="range-chip">30-45</span>
            </div>
            <input
              type="number"
              className="input-ghost"
              placeholder="30"
              value={form.exercise_minutes}
              onChange={(e) => setForm({ ...form, exercise_minutes: e.target.value })}
              required
            />
          </div>

          <div className="input-tile">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="icon-pill"><Monitor className="w-5 h-5" /></span>
                <div>
                  <p className="text-sm text-gray-300">Screen Time</p>
                  <p className="text-xs text-gray-500">Hours today</p>
                </div>
              </div>
              <span className="range-chip">&lt; 6 hrs</span>
            </div>
            <input
              type="number"
              step="0.5"
              className="input-ghost"
              placeholder="6"
              value={form.screen_time}
              onChange={(e) => setForm({ ...form, screen_time: e.target.value })}
              required
            />
          </div>

          <div className="input-tile">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="icon-pill"><Footprints className="w-5 h-5" /></span>
                <div>
                  <p className="text-sm text-gray-300">Daily Steps</p>
                  <p className="text-xs text-gray-500">Move target</p>
                </div>
              </div>
              <span className="range-chip">8k-12k</span>
            </div>
            <input
              type="number"
              className="input-ghost"
              placeholder="8000"
              value={form.daily_steps}
              onChange={(e) => setForm({ ...form, daily_steps: e.target.value })}
              required
            />
          </div>

          <div className="input-tile">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="icon-pill"><Droplets className="w-5 h-5" /></span>
                <div>
                  <p className="text-sm text-gray-300">Water Intake</p>
                  <p className="text-xs text-gray-500">Glasses today</p>
                </div>
              </div>
              <span className="range-chip">6-10</span>
            </div>
            <input
              type="number"
              className="input-ghost"
              placeholder="6"
              value={form.water_intake}
              onChange={(e) => setForm({ ...form, water_intake: e.target.value })}
            />
          </div>
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <p className="text-sm text-gray-500">We blend these habits to craft your lifestyle score.</p>
          <button type="submit" className="btn-primary w-full sm:w-auto px-6" disabled={loading}>
            {loading ? 'Analyzing...' : '📋 Get Captain\'s Orders'}
          </button>
        </div>
      </form>

      {result && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-white">Your Lifestyle Report</h3>
            <TrendingUp className="w-5 h-5 text-teal-400" />
          </div>
          <div className="mb-4">
            <div className="flex items-center gap-4">
              <div className="text-4xl font-bold text-teal-400">{result.lifestyle_score}</div>
              <div>
                <p className="text-white">Lifestyle Score</p>
                <p className="text-sm text-gray-400 capitalize">Profile: {result.cluster}</p>
              </div>
            </div>
            <div className="mt-2 h-2 bg-navy-600 rounded-full">
              <div className="h-2 bg-teal-500 rounded-full" style={{width: `${result.lifestyle_score}%`}}></div>
            </div>
          </div>
          <div>
            <p className="text-sm text-gray-400 mb-2">Captain's Orders:</p>
            <ul className="space-y-2">
              {result.recommendations.map((r, i) => (
                <li key={i} className="text-sm text-gray-300 flex items-start gap-2">
                  <span className="text-gold-500">⚓</span> {r}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default CaptainsOrders;
