import React, { useState, useEffect } from 'react';
import { Anchor, Plus, Check, Flame, Target, Trash2, Award } from 'lucide-react';

const CATEGORIES = ['health', 'fitness', 'learning', 'productivity', 'mindfulness', 'social', 'other'];

const CATEGORY_COLORS = {
  health: 'bg-green-500',
  fitness: 'bg-blue-500',
  learning: 'bg-purple-500',
  productivity: 'bg-orange-500',
  mindfulness: 'bg-teal-500',
  social: 'bg-pink-500',
  other: 'bg-gray-500'
};

function DailySails() {
  const [habits, setHabits] = useState([]);
  const [score, setScore] = useState(null);
  const [form, setForm] = useState({ name: '', category: 'health', target_days: 7 });
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // TODO: Fetch from /api/daily-sails/habits
    setHabits([
      { id: '1', name: 'Morning Exercise', category: 'fitness', current_streak: 7, completed_today: true, weekly_rate: 85, total_completions: 28 },
      { id: '2', name: 'Read 30 minutes', category: 'learning', current_streak: 3, completed_today: false, weekly_rate: 57, total_completions: 15 },
      { id: '3', name: 'Drink 8 glasses of water', category: 'health', current_streak: 12, completed_today: true, weekly_rate: 100, total_completions: 45 },
      { id: '4', name: 'Meditate 10 minutes', category: 'mindfulness', current_streak: 0, completed_today: false, weekly_rate: 28, total_completions: 8 },
    ]);
    
    // TODO: Fetch from /api/daily-sails/score
    setScore({
      score: 72,
      total_habits: 4,
      completed_today: 2,
      longest_streak: 12,
      daily_completion_rate: 50
    });
  }, []);

  const toggleHabit = async (habitId) => {
    // TODO: API call to /api/daily-sails/complete or /api/daily-sails/uncomplete
    setHabits(habits.map(h => {
      if (h.id === habitId) {
        const newCompleted = !h.completed_today;
        return {
          ...h,
          completed_today: newCompleted,
          current_streak: newCompleted ? h.current_streak + 1 : Math.max(0, h.current_streak - 1)
        };
      }
      return h;
    }));
    
    // Update score
    if (score) {
      const habit = habits.find(h => h.id === habitId);
      const change = habit?.completed_today ? -1 : 1;
      setScore({
        ...score,
        completed_today: score.completed_today + change,
        daily_completion_rate: Math.round(((score.completed_today + change) / score.total_habits) * 100)
      });
    }
  };

  const addHabit = async (e) => {
    e.preventDefault();
    if (!form.name.trim()) return;
    setLoading(true);

    // TODO: API call to /api/daily-sails/habits
    const newHabit = {
      id: Date.now().toString(),
      name: form.name,
      category: form.category,
      target_days: form.target_days,
      current_streak: 0,
      completed_today: false,
      weekly_rate: 0,
      total_completions: 0
    };
    
    setHabits([...habits, newHabit]);
    if (score) {
      setScore({ ...score, total_habits: score.total_habits + 1 });
    }
    setForm({ name: '', category: 'health', target_days: 7 });
    setShowForm(false);
    setLoading(false);
  };

  const deleteHabit = (habitId) => {
    // TODO: API call to DELETE /api/daily-sails/habits/:id
    setHabits(habits.filter(h => h.id !== habitId));
    if (score) {
      setScore({ ...score, total_habits: score.total_habits - 1 });
    }
  };

  const completedCount = habits.filter(h => h.completed_today).length;
  const progressPercent = habits.length ? (completedCount / habits.length) * 100 : 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card">
        <div className="flex items-center gap-3 mb-4">
          <Anchor className="w-6 h-6 text-blue-400" />
          <h2 className="text-xl font-bold text-white">Habit Tracker</h2>
        </div>
        <p className="text-gray-400 text-sm">Set your daily sails - consistent habits lead to successful voyages!</p>
      </div>

      {/* Daily Progress */}
      <div className="card bg-gradient-to-r from-navy-800 to-navy-700">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-semibold text-white">Today's Progress</h3>
            <p className="text-sm text-gray-400">{completedCount} of {habits.length} habits completed</p>
          </div>
          <div className="text-right">
            <span className="text-3xl font-bold text-teal-400">{Math.round(progressPercent)}%</span>
          </div>
        </div>
        <div className="h-3 bg-navy-600 rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-teal-500 to-teal-400 rounded-full transition-all duration-500"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* Stats Cards */}
      {score && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="card">
            <div className="flex items-center gap-2 mb-2">
              <Target className="w-4 h-4 text-teal-400" />
              <span className="text-sm text-gray-400">Consistency</span>
            </div>
            <p className="text-2xl font-bold text-teal-400">{score.score}%</p>
          </div>
          <div className="card">
            <div className="flex items-center gap-2 mb-2">
              <Flame className="w-4 h-4 text-orange-400" />
              <span className="text-sm text-gray-400">Best Streak</span>
            </div>
            <p className="text-2xl font-bold text-orange-400">{score.longest_streak} days</p>
          </div>
          <div className="card">
            <div className="flex items-center gap-2 mb-2">
              <Anchor className="w-4 h-4 text-blue-400" />
              <span className="text-sm text-gray-400">Active Habits</span>
            </div>
            <p className="text-2xl font-bold text-blue-400">{score.total_habits}</p>
          </div>
          <div className="card">
            <div className="flex items-center gap-2 mb-2">
              <Award className="w-4 h-4 text-gold-500" />
              <span className="text-sm text-gray-400">Today's Rate</span>
            </div>
            <p className="text-2xl font-bold text-gold-500">{score.daily_completion_rate}%</p>
          </div>
        </div>
      )}

      {/* Add Habit Button */}
      {!showForm && (
        <button 
          onClick={() => setShowForm(true)}
          className="btn-primary w-full flex items-center justify-center gap-2"
        >
          <Plus className="w-5 h-5" /> Add New Habit
        </button>
      )}

      {/* Add Habit Form */}
      {showForm && (
        <form onSubmit={addHabit} className="card space-y-4">
          <h3 className="font-semibold text-white">New Habit</h3>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <div className="lg:col-span-2">
              <label className="block text-sm text-gray-400 mb-1">Habit Name</label>
              <input 
                type="text" 
                className="input-field" 
                placeholder="e.g., Morning Exercise"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Category</label>
              <select 
                className="input-field" 
                value={form.category}
                onChange={(e) => setForm({ ...form, category: e.target.value })}
              >
                {CATEGORIES.map(cat => (
                  <option key={cat} value={cat}>{cat.charAt(0).toUpperCase() + cat.slice(1)}</option>
                ))}
              </select>
            </div>
          </div>
          <div className="flex gap-2">
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Adding...' : '⛵ Add Habit'}
            </button>
            <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 bg-navy-600 rounded-lg text-gray-300 hover:bg-navy-500">
              Cancel
            </button>
          </div>
        </form>
      )}

      {/* Habits List */}
      <div className="space-y-3">
        {habits.map(habit => (
          <div 
            key={habit.id} 
            className={`card flex items-center justify-between transition-all ${
              habit.completed_today ? 'bg-green-900/20 border-green-700/30' : ''
            }`}
          >
            <div className="flex items-center gap-4">
              <button 
                onClick={() => toggleHabit(habit.id)}
                className={`w-8 h-8 rounded-full border-2 flex items-center justify-center transition-all ${
                  habit.completed_today 
                    ? 'bg-green-500 border-green-500' 
                    : 'border-gray-500 hover:border-teal-400'
                }`}
              >
                {habit.completed_today && <Check className="w-5 h-5 text-white" />}
              </button>
              <div>
                <div className="flex items-center gap-2">
                  <span className={`w-2 h-2 rounded-full ${CATEGORY_COLORS[habit.category]}`} />
                  <h4 className={`font-medium ${habit.completed_today ? 'text-gray-400 line-through' : 'text-white'}`}>
                    {habit.name}
                  </h4>
                </div>
                <div className="flex items-center gap-3 text-xs text-gray-500 mt-1">
                  <span className="capitalize">{habit.category}</span>
                  <span>•</span>
                  <span className="flex items-center gap-1">
                    <Flame className="w-3 h-3 text-orange-400" />
                    {habit.current_streak} day streak
                  </span>
                  <span>•</span>
                  <span>{habit.weekly_rate}% this week</span>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <div className="text-right mr-4">
                <span className="text-lg font-bold text-teal-400">{habit.total_completions}</span>
                <span className="text-xs text-gray-500 block">total</span>
              </div>
              <button 
                onClick={() => deleteHabit(habit.id)}
                className="p-2 text-gray-500 hover:text-red-400 transition-colors"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {habits.length === 0 && (
        <div className="card text-center py-8">
          <Anchor className="w-12 h-12 text-gray-600 mx-auto mb-3" />
          <p className="text-gray-400">No habits yet. Set your first sail!</p>
        </div>
      )}

      {/* TODO: Add habit analytics chart */}
      {/* TODO: Add weekly calendar view */}
      {/* TODO: Add habit reminders */}
    </div>
  );
}

export default DailySails;
