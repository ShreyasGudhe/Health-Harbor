"""
Daily Sails - Habit Tracker
============================
Manages daily habits with streak tracking.

Author: VitalPlunder Team
"""

import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

class HabitManager:
    """
    Manages habits and tracks daily completions.
    Uses JSON storage for simplicity.
    """
    
    HABIT_CATEGORIES = ['health', 'fitness', 'learning', 'productivity', 'mindfulness', 'social', 'other']
    
    def __init__(self):
        self.data_dir = os.path.dirname(os.path.abspath(__file__))
        self.habits_file = os.path.join(self.data_dir, 'habits.json')
        self.completions_file = os.path.join(self.data_dir, 'completions.json')
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Create JSON files if they don't exist"""
        for filepath in [self.habits_file, self.completions_file]:
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump([], f)
    
    def _read_habits(self):
        """Read all habits"""
        try:
            with open(self.habits_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _write_habits(self, habits):
        """Write habits to file"""
        with open(self.habits_file, 'w', encoding='utf-8') as f:
            json.dump(habits, f, indent=2, ensure_ascii=False)
    
    def _read_completions(self):
        """Read all completions"""
        try:
            with open(self.completions_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _write_completions(self, completions):
        """Write completions to file"""
        with open(self.completions_file, 'w', encoding='utf-8') as f:
            json.dump(completions, f, indent=2, ensure_ascii=False)
    
    def create_habit(self, habit_name, category='other', target_days=7, description=''):
        """
        Create a new habit
        
        Args:
            habit_name: Name of the habit
            category: Habit category
            target_days: Target days per week
            description: Optional description
            
        Returns:
            dict: Created habit
        """
        if category not in self.HABIT_CATEGORIES:
            category = 'other'
        
        habit = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S%f'),
            'name': habit_name,
            'category': category,
            'description': description,
            'target_days': min(target_days, 7),
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'active': True,
            'created_at': datetime.now().isoformat()
        }
        
        habits = self._read_habits()
        habits.append(habit)
        self._write_habits(habits)
        
        return habit
    
    def get_habits(self, active_only=True):
        """
        Get all habits with streak information
        
        Args:
            active_only: Filter only active habits
            
        Returns:
            list: Habits with streak data
        """
        habits = self._read_habits()
        completions = self._read_completions()
        today = datetime.now().strftime('%Y-%m-%d')
        
        if active_only:
            habits = [h for h in habits if h.get('active', True)]
        
        # Calculate streaks and today's status
        for habit in habits:
            habit_completions = [c for c in completions if c['habit_id'] == habit['id']]
            completion_dates = sorted(set(c['date'] for c in habit_completions), reverse=True)
            
            # Check if completed today
            habit['completed_today'] = today in completion_dates
            
            # Calculate current streak
            streak = 0
            check_date = datetime.now()
            
            # If not completed today, start from yesterday
            if not habit['completed_today']:
                check_date = check_date - timedelta(days=1)
            
            for i in range(365):  # Max 1 year
                date_str = (check_date - timedelta(days=i)).strftime('%Y-%m-%d')
                if date_str in completion_dates:
                    streak += 1
                else:
                    break
            
            habit['current_streak'] = streak
            
            # Calculate weekly completion rate
            week_start = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            week_completions = len([d for d in completion_dates if d >= week_start])
            habit['weekly_rate'] = round(week_completions / 7 * 100)
            
            # Calculate total completions
            habit['total_completions'] = len(habit_completions)
        
        return habits
    
    def complete_habit(self, habit_id, date=None):
        """
        Mark a habit as completed for a date
        
        Args:
            habit_id: ID of the habit
            date: Date of completion (defaults to today)
            
        Returns:
            dict: Completion record
        """
        habits = self._read_habits()
        habit = next((h for h in habits if h['id'] == habit_id), None)
        
        if not habit:
            raise ValueError("Habit not found")
        
        date = date or datetime.now().strftime('%Y-%m-%d')
        completions = self._read_completions()
        
        # Check if already completed today
        existing = next((c for c in completions if c['habit_id'] == habit_id and c['date'] == date), None)
        if existing:
            return existing
        
        completion = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S%f'),
            'habit_id': habit_id,
            'date': date,
            'completed_at': datetime.now().isoformat()
        }
        
        completions.append(completion)
        self._write_completions(completions)
        
        return completion
    
    def uncomplete_habit(self, habit_id, date=None):
        """
        Remove completion for a habit on a date
        
        Args:
            habit_id: ID of the habit
            date: Date to uncomplete (defaults to today)
            
        Returns:
            bool: Success status
        """
        date = date or datetime.now().strftime('%Y-%m-%d')
        completions = self._read_completions()
        
        completions = [c for c in completions if not (c['habit_id'] == habit_id and c['date'] == date)]
        self._write_completions(completions)
        
        return True
    
    def delete_habit(self, habit_id):
        """Soft delete a habit by marking inactive"""
        habits = self._read_habits()
        for habit in habits:
            if habit['id'] == habit_id:
                habit['active'] = False
                break
        self._write_habits(habits)
        return True
    
    def get_consistency_score(self, days=30):
        """
        Calculate overall habit consistency score
        
        Args:
            days: Number of days to analyze
            
        Returns:
            dict: Consistency analysis
        """
        habits = self.get_habits(active_only=True)
        completions = self._read_completions()
        
        if not habits:
            return {'score': 0, 'total_habits': 0, 'completed_today': 0}
        
        today = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Calculate metrics
        total_possible = len(habits) * days
        total_completed = len([c for c in completions if c['date'] >= start_date])
        completed_today = len([h for h in habits if h['completed_today']])
        
        score = round(total_completed / total_possible * 100) if total_possible > 0 else 0
        
        # Calculate longest streak across all habits
        longest_streak = max((h['current_streak'] for h in habits), default=0)
        
        # TODO: Add ML-based habit recommendation
        # TODO: Add habit clustering analysis
        
        return {
            'score': score,
            'total_habits': len(habits),
            'completed_today': completed_today,
            'total_completions': total_completed,
            'longest_streak': longest_streak,
            'daily_completion_rate': round(completed_today / len(habits) * 100) if habits else 0
        }


# Singleton instance
_habit_manager = None

def get_habit_manager():
    global _habit_manager
    if _habit_manager is None:
        _habit_manager = HabitManager()
    return _habit_manager
