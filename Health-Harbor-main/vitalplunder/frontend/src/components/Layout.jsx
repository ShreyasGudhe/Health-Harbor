/**
 * VitalPlunder - Layout Component
 * 
 * Main layout with sidebar navigation and header.
 * 
 * @author VitalPlunder Team
 */

import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Anchor, 
  Activity, 
  Brain, 
  Compass, 
  Pill, 
  Moon, 
  Utensils, 
  FileText,
  Menu,
  X,
  Skull,
  Coins,
  BookOpen
} from 'lucide-react';

// Navigation items configuration
const navItems = [
  {
    path: '/',
    name: "Captain's Deck",
    description: 'Dashboard Overview',
    icon: Anchor,
  },
  {
    path: '/storm-watch',
    name: 'Storm Watch',
    description: 'Health Risk Scanner',
    icon: Activity,
  },
  {
    path: '/mind-compass',
    name: 'Mind Compass',
    description: 'Mental Health Monitor',
    icon: Brain,
  },
  {
    path: '/captains-orders',
    name: "Captain's Orders",
    description: 'Lifestyle Coaching',
    icon: Compass,
  },
  {
    path: '/supply-check',
    name: 'Supply Check',
    description: 'Medication Tracker',
    icon: Pill,
  },
  {
    path: '/night-watch',
    name: 'Night Watch',
    description: 'Sleep Quality',
    icon: Moon,
  },
  {
    path: '/galley-log',
    name: 'Galley Log',
    description: 'Diet & Nutrition',
    icon: Utensils,
  },
  {
    path: '/ship-doctor',
    name: 'Ship Doctor',
    description: 'Medical Documents',
    icon: FileText,
  },
  {
    path: '/treasure-ledger',
    name: 'Treasure Ledger',
    description: 'Personal Finance',
    icon: Coins,
  },
  {
    path: '/captains-log',
    name: "Captain's Log",
    description: 'Digital Diary',
    icon: BookOpen,
  },
  {
    path: '/daily-sails',
    name: 'Daily Sails',
    description: 'Habit Tracker',
    icon: Anchor,
  },
];

/**
 * Sidebar Component
 */
function Sidebar({ isOpen, onClose }) {
  const location = useLocation();
  
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <aside 
        className={`
          fixed lg:static inset-y-0 left-0 z-50
          w-72 bg-navy-800 border-r border-navy-700
          transform transition-transform duration-300 ease-in-out
          ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
      >
        {/* Logo */}
        <div className="p-6 border-b border-navy-700">
          <Link to="/" className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gold-600 rounded-lg flex items-center justify-center">
              <Skull className="w-6 h-6 text-navy-900" />
            </div>
            <div>
              <h1 className="text-xl font-pirate font-bold gradient-text">
                VitalPlunder
              </h1>
              <p className="text-xs text-gray-400">Plunder Health Risks ☠️</p>
            </div>
          </Link>
        </div>
        
        {/* Navigation */}
        <nav className="p-4 space-y-1">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            const Icon = item.icon;
            
            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={onClose}
                className={`
                  nav-link
                  ${isActive ? 'nav-link-active' : ''}
                `}
              >
                <Icon className="w-5 h-5" />
                <div>
                  <div className="font-medium">{item.name}</div>
                  <div className="text-xs text-gray-500">{item.description}</div>
                </div>
              </Link>
            );
          })}
        </nav>
        
        {/* Footer */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-navy-700">
          <div className="text-xs text-gray-500 text-center">
            <p>VitalPlunder v1.0</p>
            <p className="mt-1">⚓ Sail towards better health</p>
          </div>
        </div>
      </aside>
    </>
  );
}

/**
 * Header Component
 */
function Header({ onMenuClick }) {
  const location = useLocation();
  
  // Find current page info
  const currentPage = navItems.find(item => item.path === location.pathname) || navItems[0];
  
  return (
    <header className="bg-navy-800 border-b border-navy-700 px-4 lg:px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          {/* Mobile menu button */}
          <button 
            className="lg:hidden p-2 hover:bg-navy-700 rounded-lg"
            onClick={onMenuClick}
          >
            <Menu className="w-6 h-6" />
          </button>
          
          {/* Page title */}
          <div>
            <h2 className="text-xl font-semibold text-white flex items-center gap-2">
              <currentPage.icon className="w-5 h-5 text-teal-400" />
              {currentPage.name}
            </h2>
            <p className="text-sm text-gray-400">{currentPage.description}</p>
          </div>
        </div>
        
        {/* Right side - placeholder for user menu */}
        <div className="flex items-center gap-4">
          <div className="text-right hidden sm:block">
            <p className="text-sm text-white">Captain</p>
            <p className="text-xs text-gray-400">Ready to sail</p>
          </div>
          <div className="w-10 h-10 bg-teal-600 rounded-full flex items-center justify-center">
            <span className="text-white font-semibold">C</span>
          </div>
        </div>
      </div>
    </header>
  );
}

/**
 * Main Layout Component
 */
function Layout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  
  return (
    <div className="min-h-screen bg-navy-900 flex">
      {/* Sidebar */}
      <Sidebar 
        isOpen={sidebarOpen} 
        onClose={() => setSidebarOpen(false)} 
      />
      
      {/* Main content area */}
      <div className="flex-1 flex flex-col min-h-screen">
        {/* Header */}
        <Header onMenuClick={() => setSidebarOpen(true)} />
        
        {/* Page content */}
        <main className="flex-1 p-4 lg:p-6 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
}

export default Layout;
