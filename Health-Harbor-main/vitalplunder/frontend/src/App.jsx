/**
 * VitalPlunder - Main App Component
 * 
 * The Captain's Deck - Main navigation and routing for VitalPlunder.
 * 
 * @author VitalPlunder Team
 */

import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';

// Page imports
import Dashboard from './pages/Dashboard';
import StormWatch from './pages/StormWatch';
import MindCompass from './pages/MindCompass';
import CaptainsOrders from './pages/CaptainsOrders';
import SupplyCheck from './pages/SupplyCheck';
import NightWatch from './pages/NightWatch';
import GalleyLog from './pages/GalleyLog';
import ShipDoctor from './pages/ShipDoctor';

// New Productivity Modules
import TreasureLedger from './pages/TreasureLedger';
import CaptainsLog from './pages/CaptainsLog';
import DailySails from './pages/DailySails';

/**
 * Main Application Component
 * 
 * Sets up routing for all modules of VitalPlunder.
 */
function App() {
  return (
    <Layout>
      <Routes>
        {/* Dashboard - Captain's Deck */}
        <Route path="/" element={<Dashboard />} />
        
        {/* Module 1: Storm Watch - Health Risk Scanner */}
        <Route path="/storm-watch" element={<StormWatch />} />
        
        {/* Module 2: Mind Compass - Mental Health Monitor */}
        <Route path="/mind-compass" element={<MindCompass />} />
        
        {/* Module 3: Captain's Orders - Lifestyle Coaching */}
        <Route path="/captains-orders" element={<CaptainsOrders />} />
        
        {/* Module 4: Supply Check - Medication Adherence */}
        <Route path="/supply-check" element={<SupplyCheck />} />
        
        {/* Module 5: Night Watch - Sleep Quality */}
        <Route path="/night-watch" element={<NightWatch />} />
        
        {/* Module 6: Galley Log - Diet & Nutrition */}
        <Route path="/galley-log" element={<GalleyLog />} />
        
        {/* Module 7: Ship Doctor - Medical Documents */}
        <Route path="/ship-doctor" element={<ShipDoctor />} />
        
        {/* Module 8: Treasure Ledger - Personal Finance */}
        <Route path="/treasure-ledger" element={<TreasureLedger />} />
        
        {/* Module 9: Captain's Log - Digital Diary */}
        <Route path="/captains-log" element={<CaptainsLog />} />
        
        {/* Module 10: Daily Sails - Habit Tracker */}
        <Route path="/daily-sails" element={<DailySails />} />
      </Routes>
    </Layout>
  );
}

export default App;
