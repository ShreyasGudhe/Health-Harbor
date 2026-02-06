"""
Captain's Log - Journal Manager
================================
Handles digital diary entries with mood tracking.

Author: VitalPlunder Team
"""

import os
import json
from datetime import datetime, timedelta
from collections import Counter

class JournalManager:
    """
    Manages journal entries with mood tracking.
    Uses JSON storage for simplicity.
    """
    
    MOODS = ['happy', 'neutral', 'stressed', 'sad', 'anxious', 'excited', 'calm']
    
    MOOD_SCORES = {
        'happy': 5,
        'excited': 5,
        'calm': 4,
        'neutral': 3,
        'anxious': 2,
        'stressed': 2,
        'sad': 1
    }
    
    def __init__(self):
        self.data_dir = os.path.dirname(os.path.abspath(__file__))
        self.json_file = os.path.join(self.data_dir, 'journal_entries.json')
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create JSON file if it doesn't exist"""
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def _read_entries(self):
        """Read all journal entries"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._ensure_file_exists()
            return []
    
    def _write_entries(self, entries):
        """Write all entries to file"""
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
    
    def add_entry(self, journal_text, mood, date=None):
        """
        Add a new journal entry
        
        Args:
            journal_text: The diary content
            mood: Current mood (from MOODS list)
            date: Entry date (defaults to today)
            
        Returns:
            dict: Created entry
        """
        if mood not in self.MOODS:
            mood = 'neutral'
        
        entry = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S%f'),
            'date': date or datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M'),
            'journal_text': journal_text,
            'mood': mood,
            'mood_score': self.MOOD_SCORES.get(mood, 3),
            'word_count': len(journal_text.split()),
            'created_at': datetime.now().isoformat(),
            'sentiment': self._analyze_sentiment(journal_text)
        }
        
        entries = self._read_entries()
        entries.append(entry)
        self._write_entries(entries)
        
        return entry
    
    def _analyze_sentiment(self, text):
        """
        Basic sentiment analysis placeholder
        
        TODO: Integrate with Mind Compass NLP for better analysis
        TODO: Add ML-based emotion detection
        """
        # Simple keyword-based sentiment
        positive_words = ['happy', 'great', 'good', 'amazing', 'wonderful', 'love', 'excited', 'grateful', 'blessed', 'joy']
        negative_words = ['sad', 'angry', 'stressed', 'worried', 'anxious', 'tired', 'frustrated', 'upset', 'fear', 'hate']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        return 'neutral'
    
    def get_entries(self, start_date=None, end_date=None, mood=None, limit=50):
        """
        Get journal entries with optional filters
        
        Args:
            start_date: Filter from date
            end_date: Filter until date
            mood: Filter by mood
            limit: Max entries to return
            
        Returns:
            list: Filtered entries
        """
        entries = self._read_entries()
        
        if mood:
            entries = [e for e in entries if e['mood'] == mood]
        
        if start_date:
            entries = [e for e in entries if e['date'] >= start_date]
        
        if end_date:
            entries = [e for e in entries if e['date'] <= end_date]
        
        # Sort by date descending
        entries = sorted(entries, key=lambda x: (x['date'], x.get('time', '00:00')), reverse=True)
        
        return entries[:limit]
    
    def get_mood_trends(self, days=30):
        """
        Analyze mood trends over time
        
        Args:
            days: Number of days to analyze
            
        Returns:
            dict: Mood trend analysis
        """
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        entries = self.get_entries(start_date=start_date, limit=1000)
        
        if not entries:
            return {
                'average_mood_score': 0,
                'mood_distribution': {},
                'trend': 'neutral',
                'entries_count': 0
            }
        
        # Calculate statistics
        mood_scores = [e['mood_score'] for e in entries]
        mood_counts = Counter(e['mood'] for e in entries)
        
        avg_score = sum(mood_scores) / len(mood_scores)
        
        # Determine trend (compare first half to second half)
        if len(mood_scores) >= 4:
            mid = len(mood_scores) // 2
            first_half_avg = sum(mood_scores[mid:]) / len(mood_scores[mid:])
            second_half_avg = sum(mood_scores[:mid]) / len(mood_scores[:mid])
            
            if second_half_avg > first_half_avg + 0.5:
                trend = 'improving'
            elif second_half_avg < first_half_avg - 0.5:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'neutral'
        
        # Daily mood scores for charting
        daily_scores = {}
        for entry in entries:
            date = entry['date']
            if date not in daily_scores:
                daily_scores[date] = []
            daily_scores[date].append(entry['mood_score'])
        
        daily_averages = {date: sum(scores)/len(scores) for date, scores in daily_scores.items()}
        
        return {
            'average_mood_score': round(avg_score, 2),
            'mood_distribution': dict(mood_counts),
            'trend': trend,
            'entries_count': len(entries),
            'daily_averages': daily_averages,
            'dominant_mood': mood_counts.most_common(1)[0][0] if mood_counts else 'neutral'
        }
    
    def get_writing_streak(self):
        """
        Calculate consecutive days of journaling
        
        Returns:
            dict: Streak information
        """
        entries = self._read_entries()
        if not entries:
            return {'current_streak': 0, 'longest_streak': 0, 'total_entries': 0}
        
        # Get unique dates
        dates = sorted(set(e['date'] for e in entries), reverse=True)
        
        # Calculate current streak
        current_streak = 0
        today = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Check if today or yesterday has an entry
        if dates and (dates[0] == today or dates[0] == yesterday):
            current_streak = 1
            for i in range(1, len(dates)):
                expected = (datetime.strptime(dates[0], '%Y-%m-%d') - timedelta(days=i)).strftime('%Y-%m-%d')
                if dates[i] if i < len(dates) else None == expected:
                    current_streak += 1
                else:
                    break
        
        return {
            'current_streak': current_streak,
            'total_entries': len(entries),
            'unique_days': len(dates)
        }


# Singleton instance
_journal_manager = None

def get_journal_manager():
    global _journal_manager
    if _journal_manager is None:
        _journal_manager = JournalManager()
    return _journal_manager
