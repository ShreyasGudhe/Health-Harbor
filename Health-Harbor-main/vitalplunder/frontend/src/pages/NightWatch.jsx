import React, { useState } from 'react';
import { Moon, Sun, Clock, AlarmClock, BedDouble, Coffee, Gauge } from 'lucide-react';

function NightWatch() {
  const [form, setForm] = useState({ sleep_hours: '', bedtime: '', wake_time: '', quality: '3' });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    // TODO: API call to /api/night-watch/analyze
    // const response = await api.nightWatch.analyze(form);
    setTimeout(() => {
      setResult({
        sleep_score: 78,
        quality_rating: 'Good',
        deep_sleep_estimate: '1.5 hours',
        recommendations: ['Try to maintain consistent sleep times', 'Avoid screens 1 hour before bed']
      });
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <div className="glass-panel card bg-gradient-to-r from-navy-900/80 via-navy-800/80 to-navy-800/60 border border-indigo-500/20">
        <div className="flex items-center gap-3 mb-3">
          <Moon className="w-6 h-6 text-indigo-400" />
          <div>
            <h2 className="text-xl font-bold text-white">Sleep Quality Tracker</h2>
            <p className="text-gray-400 text-sm">Log your night watch and uncover better sleep patterns.</p>
          </div>
        </div>
        <div className="flex gap-2 text-xs text-gray-500 flex-wrap">
          <span className="range-chip">Circadian-friendly</span>
          <span className="range-chip">Screen-free reminder</span>
          <span className="range-chip">Score preview</span>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="glass-panel card space-y-5 bg-gradient-to-br from-navy-900/70 via-navy-800/70 to-navy-800/60 border border-navy-700/70">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="input-tile">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="icon-pill"><Gauge className="w-5 h-5" /></span>
                <div>
                  <p className="text-sm text-gray-300">Sleep Duration</p>
                  <p className="text-xs text-gray-500">Hours last night</p>
                </div>
              </div>
              <span className="range-chip">7-9 hrs</span>
            </div>
            <input
              type="number"
              step="0.5"
              className="input-ghost"
              placeholder="7.5"
              value={form.sleep_hours}
              onChange={(e) => setForm({ ...form, sleep_hours: e.target.value })}
              required
            />
          </div>

          <div className="input-tile">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="icon-pill"><AlarmClock className="w-5 h-5" /></span>
                <div>
                  <p className="text-sm text-gray-300">Sleep Quality</p>
                  <p className="text-xs text-gray-500">Self-rated</p>
                </div>
              </div>
              <span className="range-chip">1-5</span>
            </div>
            <select
              className="input-ghost"
              value={form.quality}
              onChange={(e) => setForm({ ...form, quality: e.target.value })}
            >
              <option value="1">1 - Very Poor</option>
              <option value="2">2 - Poor</option>
              <option value="3">3 - Average</option>
              <option value="4">4 - Good</option>
              <option value="5">5 - Excellent</option>
            </select>
          </div>

          <div className="input-tile">
            <div className="flex items-center gap-3 mb-1">
              <span className="icon-pill"><BedDouble className="w-5 h-5" /></span>
              <div>
                <p className="text-sm text-gray-300">Bedtime</p>
                <p className="text-xs text-gray-500">When you hit the bunk</p>
              </div>
            </div>
            <input
              type="time"
              className="input-ghost"
              value={form.bedtime}
              onChange={(e) => setForm({ ...form, bedtime: e.target.value })}
            />
          </div>

          <div className="input-tile">
            <div className="flex items-center gap-3 mb-1">
              <span className="icon-pill"><Coffee className="w-5 h-5" /></span>
              <div>
                <p className="text-sm text-gray-300">Wake Time</p>
                <p className="text-xs text-gray-500">Rise and shine</p>
              </div>
            </div>
            <input
              type="time"
              className="input-ghost"
              value={form.wake_time}
              onChange={(e) => setForm({ ...form, wake_time: e.target.value })}
            />
          </div>
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <p className="text-sm text-gray-500">We score duration, quality, and consistency to reveal your sleep grade.</p>
          <button type="submit" className="btn-primary w-full sm:w-auto px-6" disabled={loading}>
            {loading ? 'Analyzing...' : '🌙 Analyze Sleep'}
          </button>
        </div>
      </form>

      {result && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-white">Sleep Analysis</h3>
            <Sun className="w-5 h-5 text-yellow-400" />
          </div>
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="text-center p-3 bg-navy-700 rounded-lg">
              <div className="text-3xl font-bold text-indigo-400">{result.sleep_score}</div>
              <div className="text-xs text-gray-400">Sleep Score</div>
            </div>
            <div className="text-center p-3 bg-navy-700 rounded-lg">
              <div className="text-lg font-bold text-teal-400">{result.quality_rating}</div>
              <div className="text-xs text-gray-400">Quality</div>
            </div>
            <div className="text-center p-3 bg-navy-700 rounded-lg">
              <div className="text-lg font-bold text-purple-400">{result.deep_sleep_estimate}</div>
              <div className="text-xs text-gray-400">Deep Sleep</div>
            </div>
          </div>
          <div>
            <p className="text-sm text-gray-400 mb-2">Recommendations:</p>
            <ul className="space-y-1">
              {result.recommendations.map((r, i) => (
                <li key={i} className="text-sm text-gray-300 flex items-start gap-2">
                  <Clock className="w-4 h-4 text-indigo-400 mt-0.5" /> {r}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default NightWatch;
