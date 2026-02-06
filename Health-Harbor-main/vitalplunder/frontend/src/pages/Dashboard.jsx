import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Activity, Brain, Compass, Pill, Moon, Utensils, FileText,
  Coins, BookOpen, Anchor, TrendingUp, TrendingDown, Flame,
  Smile, AlertTriangle, Target, Zap
} from 'lucide-react';

// Health modules
const healthModules = [
  { path: '/storm-watch', name: 'Storm Watch', desc: 'Health Risk Scanner', icon: Activity, color: 'bg-red-500' },
  { path: '/mind-compass', name: 'Mind Compass', desc: 'Mental Health Monitor', icon: Brain, color: 'bg-purple-500' },
  { path: '/captains-orders', name: "Captain's Orders", desc: 'Lifestyle Coaching', icon: Compass, color: 'bg-blue-500' },
  { path: '/supply-check', name: 'Supply Check', desc: 'Medication Tracker', icon: Pill, color: 'bg-green-500' },
  { path: '/night-watch', name: 'Night Watch', desc: 'Sleep Quality', icon: Moon, color: 'bg-indigo-500' },
  { path: '/galley-log', name: 'Galley Log', desc: 'Diet & Nutrition', icon: Utensils, color: 'bg-orange-500' },
  { path: '/ship-doctor', name: 'Ship Doctor', desc: 'Medical Documents', icon: FileText, color: 'bg-teal-500' },
];

// Productivity modules
const productivityModules = [
  { path: '/treasure-ledger', name: 'Treasure Ledger', desc: 'Personal Finance', icon: Coins, color: 'bg-gold-600' },
  { path: '/captains-log', name: "Captain's Log", desc: 'Digital Diary', icon: BookOpen, color: 'bg-amber-500' },
  { path: '/daily-sails', name: 'Daily Sails', desc: 'Habit Tracker', icon: Anchor, color: 'bg-cyan-500' },
];

function Dashboard() {
  // TODO: Fetch real data from APIs
  const [stats, setStats] = useState({
    // Finance
    todayExpenses: 45,
    monthlyBudget: 1000,
    budgetUsed: 68,
    // Mood
    currentMood: 'happy',
    moodScore: 4,
    moodTrend: 'stable',
    // Habits
    habitsCompleted: 3,
    totalHabits: 5,
    bestStreak: 12,
    // Sleep
    lastSleepScore: 78,
    avgSleepHours: 7.2,
    // Computed Focus Score
    focusScore: 0
  });

  useEffect(() => {
    // Calculate Daily Focus Score (formula-based)
    // Focus = (Habit Rate * 0.4) + (Mood Score * 0.3) + (Sleep Score * 0.3)
    const habitRate = (stats.habitsCompleted / stats.totalHabits) * 100;
    const moodPercent = (stats.moodScore / 5) * 100;
    const sleepPercent = stats.lastSleepScore;
    
    const focusScore = Math.round(
      (habitRate * 0.4) + (moodPercent * 0.3) + (sleepPercent * 0.3)
    );
    
    setStats(prev => ({ ...prev, focusScore }));
  }, [stats.habitsCompleted, stats.totalHabits, stats.moodScore, stats.lastSleepScore]);

  const getMoodEmoji = (mood) => {
    const moods = { happy: '😊', excited: '🤩', calm: '😌', neutral: '😐', anxious: '😰', stressed: '😫', sad: '😢' };
    return moods[mood] || '😐';
  };

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="card bg-gradient-to-r from-navy-800 to-navy-700">
        <h2 className="text-2xl font-bold text-white mb-2">Welcome aboard, Captain! ⚓</h2>
        <p className="text-gray-400">Your unified command center for health, wealth, and productivity.</p>
      </div>

      {/* Daily Focus Score - Main Metric */}
      <div className="card bg-gradient-to-r from-teal-900/50 to-navy-800 border-teal-700/30">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <Zap className="w-5 h-5 text-teal-400" />
              <span className="text-gray-400">Daily Focus Score</span>
            </div>
            <p className="text-4xl font-bold text-teal-400">{stats.focusScore}</p>
            <p className="text-sm text-gray-500 mt-1">Based on habits + mood + sleep</p>
          </div>
          <div className="w-24 h-24 relative">
            <svg className="w-full h-full transform -rotate-90">
              <circle cx="48" cy="48" r="40" stroke="#1e3a5f" strokeWidth="8" fill="none" />
              <circle 
                cx="48" cy="48" r="40" 
                stroke="#14b8a6" 
                strokeWidth="8" 
                fill="none"
                strokeDasharray={`${stats.focusScore * 2.51} 251`}
                strokeLinecap="round"
              />
            </svg>
            <span className="absolute inset-0 flex items-center justify-center text-2xl font-bold text-white">
              {stats.focusScore}%
            </span>
          </div>
        </div>
      </div>

      {/* Quick Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Budget Widget */}
        <Link to="/treasure-ledger" className="card hover:border-gold-500 transition-colors">
          <div className="flex items-center gap-2 mb-2">
            <Coins className="w-4 h-4 text-gold-500" />
            <span className="text-sm text-gray-400">Today's Spending</span>
          </div>
          <p className="text-2xl font-bold text-white">${stats.todayExpenses}</p>
          <div className="mt-2">
            <div className="flex justify-between text-xs mb-1">
              <span className="text-gray-500">Budget</span>
              <span className={stats.budgetUsed > 80 ? 'text-red-400' : 'text-gray-400'}>{stats.budgetUsed}%</span>
            </div>
            <div className="h-1.5 bg-navy-600 rounded-full">
              <div 
                className={`h-1.5 rounded-full ${stats.budgetUsed > 80 ? 'bg-red-500' : 'bg-gold-500'}`}
                style={{ width: `${Math.min(stats.budgetUsed, 100)}%` }}
              />
            </div>
          </div>
        </Link>

        {/* Mood Widget */}
        <Link to="/captains-log" className="card hover:border-purple-500 transition-colors">
          <div className="flex items-center gap-2 mb-2">
            <Smile className="w-4 h-4 text-purple-400" />
            <span className="text-sm text-gray-400">Current Mood</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-3xl">{getMoodEmoji(stats.currentMood)}</span>
            <div>
              <p className="text-lg font-bold text-white capitalize">{stats.currentMood}</p>
              <p className="text-xs text-gray-500">Trend: {stats.moodTrend}</p>
            </div>
          </div>
        </Link>

        {/* Habits Widget */}
        <Link to="/daily-sails" className="card hover:border-cyan-500 transition-colors">
          <div className="flex items-center gap-2 mb-2">
            <Target className="w-4 h-4 text-cyan-400" />
            <span className="text-sm text-gray-400">Habits Today</span>
          </div>
          <p className="text-2xl font-bold text-white">
            {stats.habitsCompleted}<span className="text-gray-500">/{stats.totalHabits}</span>
          </p>
          <div className="flex items-center gap-1 mt-2 text-xs text-orange-400">
            <Flame className="w-3 h-3" />
            <span>Best streak: {stats.bestStreak} days</span>
          </div>
        </Link>

        {/* Sleep Widget */}
        <Link to="/night-watch" className="card hover:border-indigo-500 transition-colors">
          <div className="flex items-center gap-2 mb-2">
            <Moon className="w-4 h-4 text-indigo-400" />
            <span className="text-sm text-gray-400">Sleep Score</span>
          </div>
          <p className="text-2xl font-bold text-indigo-400">{stats.lastSleepScore}</p>
          <p className="text-xs text-gray-500 mt-1">Avg: {stats.avgSleepHours}h / night</p>
        </Link>
      </div>

      {/* Spending Alert */}
      {stats.budgetUsed > 80 && (
        <div className="card bg-red-900/20 border-red-700/30 flex items-center gap-3">
          <AlertTriangle className="w-5 h-5 text-red-400" />
          <div>
            <p className="text-red-300 font-medium">Spending Alert</p>
            <p className="text-sm text-gray-400">You've used {stats.budgetUsed}% of your monthly budget.</p>
          </div>
        </div>
      )}

      {/* Productivity Modules */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-teal-400" />
          Productivity Tools
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {productivityModules.map((m) => (
            <Link key={m.path} to={m.path} className="card hover:border-teal-500 transition-colors group">
              <div className="flex items-start gap-4">
                <div className={`${m.color} p-3 rounded-lg`}>
                  <m.icon className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white group-hover:text-teal-400">{m.name}</h3>
                  <p className="text-sm text-gray-400">{m.desc}</p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Health Modules */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
          <Activity className="w-5 h-5 text-red-400" />
          Health & Wellness
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {healthModules.map((m) => (
            <Link key={m.path} to={m.path} className="card hover:border-teal-500 transition-colors group">
              <div className="flex items-start gap-4">
                <div className={`${m.color} p-3 rounded-lg`}>
                  <m.icon className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white group-hover:text-teal-400">{m.name}</h3>
                  <p className="text-sm text-gray-400">{m.desc}</p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Disclaimer */}
      <div className="card bg-navy-700/50 border-gold-600/30">
        <p className="text-sm text-gray-400 text-center">
          ⚠️ VitalPlunder provides wellness insights only. Always consult healthcare professionals for medical advice.
        </p>
      </div>

      {/* TODO: Add weekly summary chart */}
      {/* TODO: Add personalized recommendations */}
      {/* TODO: Add achievement badges */}
    </div>
  );
}

export default Dashboard;
