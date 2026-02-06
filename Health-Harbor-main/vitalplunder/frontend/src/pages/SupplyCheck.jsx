import React, { useState } from 'react';
import { Pill, Plus, Bell, Check, Clock3 } from 'lucide-react';

function SupplyCheck() {
  const [medications, setMedications] = useState([
    { id: 1, name: 'Vitamin D', time: '08:00', taken: true },
    { id: 2, name: 'Omega-3', time: '12:00', taken: false },
  ]);
  const [newMed, setNewMed] = useState({ name: '', time: '' });

  const addMedication = (e) => {
    e.preventDefault();
    if (!newMed.name || !newMed.time) return;
    // TODO: API call to /api/supply-check/medications POST
    setMedications([...medications, { id: Date.now(), ...newMed, taken: false }]);
    setNewMed({ name: '', time: '' });
  };

  const toggleTaken = (id) => {
    // TODO: API call to /api/supply-check/log
    setMedications(medications.map(m => m.id === id ? {...m, taken: !m.taken} : m));
  };

  const adherenceRate = medications.length ? Math.round((medications.filter(m => m.taken).length / medications.length) * 100) : 0;

  return (
    <div className="space-y-6 max-w-2xl">
      <div className="glass-panel card bg-gradient-to-r from-navy-900/80 via-navy-800/80 to-navy-800/60 border border-green-500/20">
        <div className="flex items-center gap-3 mb-3">
          <Pill className="w-6 h-6 text-green-400" />
          <div>
            <h2 className="text-xl font-bold text-white">Medication Tracker</h2>
            <p className="text-gray-400 text-sm">Keep your medical supplies in check. Never miss a dose.</p>
          </div>
        </div>
        <div className="flex gap-2 text-xs text-gray-500 flex-wrap">
          <span className="range-chip">Smart reminders</span>
          <span className="range-chip">Adherence radar</span>
          <span className="range-chip">Private to your device</span>
        </div>
      </div>

      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold text-white">Today's Adherence</h3>
          <Bell className="w-5 h-5 text-yellow-400" />
        </div>
        <div className="flex items-center gap-4">
          <div className={`text-4xl font-bold ${adherenceRate >= 80 ? 'text-green-400' : adherenceRate >= 50 ? 'text-yellow-400' : 'text-red-400'}`}>
            {adherenceRate}%
          </div>
          <div className="flex-1">
            <div className="h-3 bg-navy-600 rounded-full">
              <div className={`h-3 rounded-full ${adherenceRate >= 80 ? 'bg-green-500' : adherenceRate >= 50 ? 'bg-yellow-500' : 'bg-red-500'}`} style={{width: `${adherenceRate}%`}}></div>
            </div>
          </div>
        </div>
      </div>

      <div className="glass-panel card bg-gradient-to-br from-navy-900/70 via-navy-800/70 to-navy-800/60 border border-navy-700/70">
        <h3 className="font-semibold text-white mb-4">Medications</h3>
        <div className="space-y-2 mb-4">
          {medications.map(med => (
            <div key={med.id} className={`flex items-center justify-between p-3 rounded-lg border ${med.taken ? 'bg-green-900/20 border-green-700/40' : 'bg-navy-800/70 border-navy-700/70'}`}>
              <div className="flex items-center gap-3">
                <button onClick={() => toggleTaken(med.id)} className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${med.taken ? 'bg-green-500 border-green-500' : 'border-gray-500 hover:border-teal-400'}`}>
                  {med.taken && <Check className="w-4 h-4 text-white" />}
                </button>
                <div>
                  <p className={`font-medium ${med.taken ? 'text-gray-400 line-through' : 'text-white'}`}>{med.name}</p>
                  <p className="text-xs text-gray-500 flex items-center gap-1"><Clock3 className="w-3 h-3" /> {med.time}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <form onSubmit={addMedication} className="grid grid-cols-1 sm:grid-cols-[1fr_auto_auto] gap-3 items-center">
          <div className="input-tile">
            <label className="text-sm text-gray-300">Medication name</label>
            <input type="text" className="input-ghost" placeholder="Vitamin D" value={newMed.name} onChange={(e) => setNewMed({...newMed, name: e.target.value})} />
          </div>
          <div className="input-tile">
            <label className="text-sm text-gray-300">Time</label>
            <input type="time" className="input-ghost" value={newMed.time} onChange={(e) => setNewMed({...newMed, time: e.target.value})} />
          </div>
          <button type="submit" className="btn-primary px-4 h-full" aria-label="Add medication"><Plus className="w-5 h-5" /></button>
        </form>
      </div>
    </div>
  );
}

export default SupplyCheck;
