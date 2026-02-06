import React, { useState, useEffect } from 'react';
import { Coins, Plus, TrendingUp, TrendingDown, PieChart, AlertTriangle } from 'lucide-react';

const EXPENSE_CATEGORIES = ['food', 'transport', 'utilities', 'entertainment', 'health', 'shopping', 'education', 'other'];
const INCOME_CATEGORIES = ['salary', 'freelance', 'investment', 'gift', 'refund', 'other'];

function TreasureLedger() {
  const [transactions, setTransactions] = useState([]);
  const [summary, setSummary] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [form, setForm] = useState({ type: 'expense', amount: '', category: 'food', description: '' });
  const [budget, setBudget] = useState(1000);
  const [loading, setLoading] = useState(false);

  // TODO: Replace with actual API calls
  useEffect(() => {
    // Simulate loading data
    setSummary({
      total_income: 3500,
      total_expense: 1850,
      balance: 1650,
      savings_rate: 47.1,
      expense_breakdown: { food: 450, transport: 200, utilities: 300, entertainment: 400, health: 150, shopping: 350 }
    });
    setTransactions([
      { id: '1', type: 'income', amount: 3500, category: 'salary', description: 'Monthly salary', date: '2026-01-01' },
      { id: '2', type: 'expense', amount: 450, category: 'food', description: 'Groceries', date: '2026-01-10' },
      { id: '3', type: 'expense', amount: 200, category: 'transport', description: 'Gas', date: '2026-01-12' },
    ]);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.amount) return;
    setLoading(true);

    // TODO: API call to /api/treasure-ledger/transaction
    // const response = await api.treasureLedger.addTransaction(form);
    
    const newTransaction = {
      id: Date.now().toString(),
      ...form,
      amount: parseFloat(form.amount),
      date: new Date().toISOString().split('T')[0]
    };
    
    setTransactions([newTransaction, ...transactions]);
    
    // Update summary
    if (summary) {
      const newSummary = { ...summary };
      if (form.type === 'income') {
        newSummary.total_income += parseFloat(form.amount);
      } else {
        newSummary.total_expense += parseFloat(form.amount);
      }
      newSummary.balance = newSummary.total_income - newSummary.total_expense;
      newSummary.savings_rate = newSummary.total_income > 0 
        ? (newSummary.balance / newSummary.total_income * 100) 
        : 0;
      setSummary(newSummary);
    }
    
    setForm({ ...form, amount: '', description: '' });
    setLoading(false);
  };

  const categories = form.type === 'income' ? INCOME_CATEGORIES : EXPENSE_CATEGORIES;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card">
        <div className="flex items-center gap-3 mb-4">
          <Coins className="w-6 h-6 text-gold-500" />
          <h2 className="text-xl font-bold text-white">Personal Finance Tracker</h2>
        </div>
        <p className="text-gray-400 text-sm">Track your doubloons - every coin counts on this voyage!</p>
      </div>

      {/* Alerts */}
      {summary && summary.total_expense > budget * 0.8 && (
        <div className="card bg-red-900/20 border-red-700/30">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-red-400" />
            <span className="text-red-300">
              {summary.total_expense > budget 
                ? `Over budget! Spent $${summary.total_expense.toFixed(0)} of $${budget} budget`
                : `Warning: ${((summary.total_expense / budget) * 100).toFixed(0)}% of monthly budget used`
              }
            </span>
          </div>
        </div>
      )}

      {/* Summary Cards */}
      {summary && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="card bg-green-900/20 border-green-700/30">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="w-4 h-4 text-green-400" />
              <span className="text-sm text-gray-400">Income</span>
            </div>
            <p className="text-2xl font-bold text-green-400">${summary.total_income.toLocaleString()}</p>
          </div>
          <div className="card bg-red-900/20 border-red-700/30">
            <div className="flex items-center gap-2 mb-2">
              <TrendingDown className="w-4 h-4 text-red-400" />
              <span className="text-sm text-gray-400">Expenses</span>
            </div>
            <p className="text-2xl font-bold text-red-400">${summary.total_expense.toLocaleString()}</p>
          </div>
          <div className="card">
            <div className="flex items-center gap-2 mb-2">
              <Coins className="w-4 h-4 text-gold-500" />
              <span className="text-sm text-gray-400">Balance</span>
            </div>
            <p className={`text-2xl font-bold ${summary.balance >= 0 ? 'text-teal-400' : 'text-red-400'}`}>
              ${summary.balance.toLocaleString()}
            </p>
          </div>
          <div className="card">
            <div className="flex items-center gap-2 mb-2">
              <PieChart className="w-4 h-4 text-purple-400" />
              <span className="text-sm text-gray-400">Savings Rate</span>
            </div>
            <p className="text-2xl font-bold text-purple-400">{summary.savings_rate.toFixed(1)}%</p>
          </div>
        </div>
      )}

      {/* Add Transaction Form */}
      <form onSubmit={handleSubmit} className="glass-panel card space-y-5 bg-gradient-to-br from-navy-900/70 via-navy-800/70 to-navy-800/60 border border-navy-700/70">
        <div className="flex items-center gap-2 text-white font-semibold">
          <Plus className="w-5 h-5" /> Add Transaction
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
          <div className="input-tile">
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-300">Type</div>
              <span className="range-chip">Income/Expense</span>
            </div>
            <select 
              className="input-ghost" 
              value={form.type} 
              onChange={(e) => setForm({...form, type: e.target.value, category: e.target.value === 'income' ? 'salary' : 'food'})}
            >
              <option value="expense">Expense</option>
              <option value="income">Income</option>
            </select>
          </div>

          <div className="input-tile">
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-300">Amount</div>
              <span className="range-chip">$</span>
            </div>
            <input 
              type="number" 
              step="0.01" 
              className="input-ghost" 
              placeholder="0.00"
              value={form.amount}
              onChange={(e) => setForm({...form, amount: e.target.value})}
              required
            />
          </div>

          <div className="input-tile">
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-300">Category</div>
              <span className="range-chip">Smart tags</span>
            </div>
            <select 
              className="input-ghost" 
              value={form.category} 
              onChange={(e) => setForm({...form, category: e.target.value})}
            >
              {categories.map(cat => (
                <option key={cat} value={cat}>{cat.charAt(0).toUpperCase() + cat.slice(1)}</option>
              ))}
            </select>
          </div>

          <div className="input-tile">
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-300">Description</div>
              <span className="range-chip">Optional</span>
            </div>
            <input 
              type="text" 
              className="input-ghost" 
              placeholder="Optional note"
              value={form.description}
              onChange={(e) => setForm({...form, description: e.target.value})}
            />
          </div>
        </div>
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <p className="text-sm text-gray-500">Track type, amount, category, and notes in one clean swoop.</p>
          <button type="submit" className="btn-primary w-full sm:w-auto px-6" disabled={loading}>
            {loading ? 'Adding...' : '💰 Add Transaction'}
          </button>
        </div>
      </form>

      {/* Budget Setting */}
      <div className="glass-panel card bg-gradient-to-br from-navy-900/70 via-navy-800/70 to-navy-800/60 border border-teal-500/20">
        <div className="flex items-center justify-between gap-3 flex-wrap">
          <div>
            <h3 className="font-semibold text-white">Monthly Budget</h3>
            <p className="text-sm text-gray-400">Set your spending limit</p>
          </div>
          <div className="input-tile w-full sm:w-auto">
            <label className="text-sm text-gray-300">Budget ($)</label>
            <input 
              type="number" 
              className="input-ghost w-full" 
              value={budget}
              onChange={(e) => setBudget(parseFloat(e.target.value) || 0)}
            />
          </div>
        </div>
        {summary && (
          <div className="mt-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-400">Spent</span>
              <span className="text-white">${summary.total_expense} / ${budget}</span>
            </div>
            <div className="h-2 bg-navy-700 rounded-full overflow-hidden">
              <div 
                className={`h-2 rounded-full ${summary.total_expense > budget ? 'bg-red-500' : summary.total_expense > budget * 0.8 ? 'bg-yellow-500' : 'bg-green-500'}`}
                style={{width: `${Math.min((summary.total_expense / budget) * 100, 100)}%`}}
              />
            </div>
          </div>
        )}
      </div>

      {/* Recent Transactions */}
      <div className="card">
        <h3 className="font-semibold text-white mb-4">Recent Transactions</h3>
        <div className="space-y-2">
          {transactions.slice(0, 10).map(t => (
            <div key={t.id} className="flex items-center justify-between p-3 bg-navy-700 rounded-lg">
              <div className="flex items-center gap-3">
                <div className={`w-2 h-2 rounded-full ${t.type === 'income' ? 'bg-green-500' : 'bg-red-500'}`} />
                <div>
                  <p className="text-white">{t.description || t.category}</p>
                  <p className="text-xs text-gray-500">{t.date} • {t.category}</p>
                </div>
              </div>
              <span className={`font-semibold ${t.type === 'income' ? 'text-green-400' : 'text-red-400'}`}>
                {t.type === 'income' ? '+' : '-'}${t.amount.toLocaleString()}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* TODO: Add expense breakdown chart */}
      {/* TODO: Add spending trends over time */}
      {/* TODO: Add ML-based spending predictions */}
    </div>
  );
}

export default TreasureLedger;
