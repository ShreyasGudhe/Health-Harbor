import React, { useState, useEffect } from 'react';
import { BookOpen, Plus, Smile, Frown, Meh, Calendar, TrendingUp, Flame } from 'lucide-react';

const MOODS = [
  { value: 'happy', label: 'Happy', emoji: '😊', color: 'bg-green-500' },
  { value: 'excited', label: 'Excited', emoji: '🤩', color: 'bg-yellow-500' },
  { value: 'calm', label: 'Calm', emoji: '😌', color: 'bg-blue-500' },
  { value: 'neutral', label: 'Neutral', emoji: '😐', color: 'bg-gray-500' },
  { value: 'anxious', label: 'Anxious', emoji: '😰', color: 'bg-orange-500' },
  { value: 'stressed', label: 'Stressed', emoji: '😫', color: 'bg-red-400' },
  { value: 'sad', label: 'Sad', emoji: '😢', color: 'bg-purple-500' },
];

function CaptainsLog() {
  const [entries, setEntries] = useState([]);
  const [trends, setTrends] = useState(null);
  const [form, setForm] = useState({ journal_text: '', mood: 'neutral' });
  const [loading, setLoading] = useState(false);
  const [streak, setStreak] = useState({ current_streak: 0, total_entries: 0 });

  useEffect(() => {
    // TODO: Fetch from /api/captains-log/history
    setEntries([
      { id: '1', date: '2026-01-16', time: '21:30', journal_text: 'Had a productive day at work. Finished the main feature.', mood: 'happy', sentiment: 'positive' },
      { id: '2', date: '2026-01-15', time: '22:00', journal_text: 'Feeling a bit overwhelmed with deadlines.', mood: 'stressed', sentiment: 'negative' },
      { id: '3', date: '2026-01-14', time: '20:45', journal_text: 'Regular day. Nothing special happened.', mood: 'neutral', sentiment: 'neutral' },
    ]);
    
    // TODO: Fetch from /api/captains-log/mood-trends
    setTrends({
      average_mood_score: 3.5,
      trend: 'stable',
      dominant_mood: 'neutral',
      entries_count: 15
    });
    
    setStreak({ current_streak: 3, total_entries: 15 });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.journal_text.trim()) return;
    setLoading(true);

    // TODO: API call to /api/captains-log/add
    const newEntry = {
      id: Date.now().toString(),
      date: new Date().toISOString().split('T')[0],
      time: new Date().toTimeString().slice(0, 5),
      journal_text: form.journal_text,
      mood: form.mood,
      sentiment: 'neutral'
    };
    
    setEntries([newEntry, ...entries]);
    setStreak({ ...streak, current_streak: streak.current_streak + 1, total_entries: streak.total_entries + 1 });
    setForm({ journal_text: '', mood: 'neutral' });
    setLoading(false);
  };

  const getMoodInfo = (mood) => MOODS.find(m => m.value === mood) || MOODS[3];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card">
        <div className="flex items-center gap-3 mb-4">
          <BookOpen className="w-6 h-6 text-amber-400" />
          <h2 className="text-xl font-bold text-white">Digital Diary & Mood Tracker</h2>
        </div>
        <p className="text-gray-400 text-sm">Record your daily voyage - thoughts, feelings, and experiences.</p>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="card">
          <div className="flex items-center gap-2 mb-2">
            <Flame className="w-4 h-4 text-orange-400" />
            <span className="text-sm text-gray-400">Writing Streak</span>
          </div>
          <p className="text-2xl font-bold text-orange-400">{streak.current_streak} days</p>
        </div>
        <div className="card">
          <div className="flex items-center gap-2 mb-2">
            <Calendar className="w-4 h-4 text-blue-400" />
            <span className="text-sm text-gray-400">Total Entries</span>
          </div>
          <p className="text-2xl font-bold text-blue-400">{streak.total_entries}</p>
        </div>
        <div className="card">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-4 h-4 text-teal-400" />
            <span className="text-sm text-gray-400">Mood Trend</span>
          </div>
          <p className="text-lg font-bold text-teal-400 capitalize">{trends?.trend || 'Stable'}</p>
        </div>
        <div className="card">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-lg">{getMoodInfo(trends?.dominant_mood).emoji}</span>
            <span className="text-sm text-gray-400">Dominant Mood</span>
          </div>
          <p className="text-lg font-bold text-white capitalize">{trends?.dominant_mood || 'Neutral'}</p>
        </div>
      </div>

      {/* New Entry Form */}
      <form onSubmit={handleSubmit} className="glass-panel card space-y-5 bg-gradient-to-br from-navy-900/70 via-navy-800/70 to-navy-800/60 border border-navy-700/70">
        <h3 className="font-semibold text-white flex items-center gap-2">
          <Plus className="w-5 h-5" /> New Journal Entry
        </h3>
        
        {/* Mood Selector */}
        <div>
          <label className="block text-sm text-gray-400 mb-2">How are you feeling?</label>
          <div className="flex flex-wrap gap-2">
            {MOODS.map(mood => (
              <button
                key={mood.value}
                type="button"
                onClick={() => setForm({ ...form, mood: mood.value })}
                className={`px-3 py-2 rounded-lg border transition-all flex items-center gap-2 ${
                  form.mood === mood.value 
                    ? `${mood.color} border-transparent text-white` 
                    : 'border-navy-600 bg-navy-700 text-gray-300 hover:border-gray-500'
                }`}
              >
                <span>{mood.emoji}</span>
                <span className="text-sm">{mood.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Journal Text */}
        <div className="input-tile">
          <div className="flex items-center justify-between mb-2">
            <div className="text-sm text-gray-300">What's on your mind?</div>
            <span className="range-chip">2-6 lines</span>
          </div>
          <textarea
            className="input-ghost min-h-[160px] resize-none"
            placeholder="Write about your day, thoughts, feelings, gratitude, goals..."
            value={form.journal_text}
            onChange={(e) => setForm({ ...form, journal_text: e.target.value })}
            required
          />
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <span className="text-sm text-gray-500">{form.journal_text.split(/\s+/).filter(Boolean).length} words</span>
          <button type="submit" className="btn-primary w-full sm:w-auto px-6" disabled={loading || !form.journal_text.trim()}>
            {loading ? 'Saving...' : '📝 Save Entry'}
          </button>
        </div>
      </form>

      {/* Journal History */}
      <div className="card">
        <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
          <Calendar className="w-5 h-5" /> Recent Entries
        </h3>
        <div className="space-y-4">
          {entries.map(entry => {
            const moodInfo = getMoodInfo(entry.mood);
            return (
              <div key={entry.id} className="p-4 bg-navy-700 rounded-lg border-l-4" style={{ borderColor: moodInfo.color.replace('bg-', '#') }}>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{moodInfo.emoji}</span>
                    <span className="text-sm text-gray-400">{entry.date} at {entry.time}</span>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded ${
                    entry.sentiment === 'positive' ? 'bg-green-900 text-green-300' :
                    entry.sentiment === 'negative' ? 'bg-red-900 text-red-300' :
                    'bg-gray-700 text-gray-300'
                  }`}>
                    {entry.sentiment}
                  </span>
                </div>
                <p className="text-gray-300 text-sm leading-relaxed">{entry.journal_text}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* TODO: Add mood chart visualization */}
      {/* TODO: Add journal reminders */}
      {/* TODO: Add search/filter functionality */}
      {/* TODO: Add export to PDF feature */}
    </div>
  );
}

export default CaptainsLog;
