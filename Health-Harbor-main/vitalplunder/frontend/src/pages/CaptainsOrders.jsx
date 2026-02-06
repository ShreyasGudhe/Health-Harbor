import React, { useState } from 'react';
import { Compass, TrendingUp } from 'lucide-react';

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
      <div className="card">
        <div className="flex items-center gap-3 mb-4">
          <Compass className="w-6 h-6 text-blue-400" />
          <h2 className="text-xl font-bold text-white">Lifestyle Coaching</h2>
        </div>
        <p className="text-gray-400 text-sm">Log your daily habits and receive personalized orders from the captain.</p>
      </div>

      <form onSubmit={handleSubmit} className="card space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm text-gray-400 mb-1">Exercise (minutes)</label>
            <input type="number" className="input-field" placeholder="30" value={form.exercise_minutes} onChange={(e) => setForm({...form, exercise_minutes: e.target.value})} required />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Screen Time (hours)</label>
            <input type="number" step="0.5" className="input-field" placeholder="6" value={form.screen_time} onChange={(e) => setForm({...form, screen_time: e.target.value})} required />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Daily Steps</label>
            <input type="number" className="input-field" placeholder="8000" value={form.daily_steps} onChange={(e) => setForm({...form, daily_steps: e.target.value})} required />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Water Intake (glasses)</label>
            <input type="number" className="input-field" placeholder="6" value={form.water_intake} onChange={(e) => setForm({...form, water_intake: e.target.value})} />
          </div>
        </div>
        <button type="submit" className="btn-primary w-full" disabled={loading}>
          {loading ? 'Analyzing...' : '📋 Get Captain\'s Orders'}
        </button>
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
