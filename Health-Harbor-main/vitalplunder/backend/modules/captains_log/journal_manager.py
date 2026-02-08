"""Captain's Log storage manager."""

import json
import logging
import os
from collections import Counter
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError

from modules.database import Base, engine, has_database, session_scope
from .models import JournalEntry


class JournalManager:
    """Manages journal entries using PostgreSQL when configured, else JSON."""

    MOODS = ['happy', 'neutral', 'stressed', 'sad', 'anxious', 'excited', 'calm']

    MOOD_SCORES = {
        'happy': 5,
        'excited': 5,
        'calm': 4,
        'neutral': 3,
        'anxious': 2,
        'stressed': 2,
        'sad': 1,
    }

    def __init__(self):
        self.data_dir = os.path.dirname(os.path.abspath(__file__))
        self.json_file = os.path.join(self.data_dir, 'journal_entries.json')
        self.use_database = has_database()

        if self.use_database and engine is not None:
            # Ensure tables exist when a database URL is configured
            Base.metadata.create_all(bind=engine)
        else:
            self._ensure_file_exists()

    # ---------------------------------------------------------------------
    # File-based helpers (fallback when DATABASE_URL is absent)
    # ---------------------------------------------------------------------
    def _ensure_file_exists(self):
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w', encoding='utf-8') as handle:
                json.dump([], handle)

    def _read_entries_file(self) -> List[dict]:
        try:
            with open(self.json_file, 'r', encoding='utf-8') as handle:
                return json.load(handle)
        except (FileNotFoundError, json.JSONDecodeError):
            self._ensure_file_exists()
            return []

    def _write_entries_file(self, entries: List[dict]):
        with open(self.json_file, 'w', encoding='utf-8') as handle:
            json.dump(entries, handle, indent=2, ensure_ascii=False)

    # ---------------------------------------------------------------------
    # Database helpers
    # ---------------------------------------------------------------------
    def _save_entry_db(self, payload: dict) -> dict:
        try:
            with session_scope() as session:
                record = JournalEntry.from_payload(payload)
                session.add(record)
                session.flush()
                session.refresh(record)
                return record.to_dict()
        except SQLAlchemyError as exc:
            logging.error("Captain's Log: failed to persist entry (%s)", exc)
            raise

    def _query_entries_db(
        self,
        start_date: Optional[str],
        end_date: Optional[str],
        mood: Optional[str],
        limit: int,
    ) -> List[dict]:
        try:
            with session_scope() as session:
                query = session.query(JournalEntry)
                if mood:
                    query = query.filter(JournalEntry.mood == mood)
                if start_date:
                    query = query.filter(JournalEntry.date >= start_date)
                if end_date:
                    query = query.filter(JournalEntry.date <= end_date)
                query = query.order_by(JournalEntry.date.desc(), JournalEntry.time.desc())
                if limit:
                    query = query.limit(limit)
                return [entry.to_dict() for entry in query.all()]
        except SQLAlchemyError as exc:
            logging.error("Captain's Log: failed to query entries (%s)", exc)
            return []

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def add_entry(self, journal_text: str, mood: str, date: Optional[str] = None) -> dict:
        if mood not in self.MOODS:
            mood = 'neutral'

        now = datetime.now()
        payload = {
            'id': now.strftime('%Y%m%d%H%M%S%f'),
            'date': date or now.strftime('%Y-%m-%d'),
            'time': now.strftime('%H:%M'),
            'journal_text': journal_text,
            'mood': mood,
            'mood_score': self.MOOD_SCORES.get(mood, 3),
            'word_count': len(journal_text.split()),
            'created_at': now.isoformat(),
            'sentiment': self._analyze_sentiment(journal_text),
        }

        if self.use_database:
            return self._save_entry_db(payload)

        entries = self._read_entries_file()
        entries.append(payload)
        self._write_entries_file(entries)
        return payload

    def get_entries(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        mood: Optional[str] = None,
        limit: int = 50,
    ) -> List[dict]:
        if self.use_database:
            return self._query_entries_db(start_date, end_date, mood, limit)

        entries = self._read_entries_file()
        if mood:
            entries = [entry for entry in entries if entry['mood'] == mood]
        if start_date:
            entries = [entry for entry in entries if entry['date'] >= start_date]
        if end_date:
            entries = [entry for entry in entries if entry['date'] <= end_date]

        entries = sorted(entries, key=lambda x: (x['date'], x.get('time', '00:00')), reverse=True)
        return entries[:limit]

    def get_mood_trends(self, days: int = 30) -> dict:
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        entries = self.get_entries(start_date=start_date, limit=1000)

        if not entries:
            return {
                'average_mood_score': 0,
                'mood_distribution': {},
                'trend': 'neutral',
                'entries_count': 0,
            }

        mood_scores = [entry['mood_score'] for entry in entries]
        mood_counts = Counter(entry['mood'] for entry in entries)
        avg_score = sum(mood_scores) / len(mood_scores)

        if len(mood_scores) >= 4:
            mid = len(mood_scores) // 2
            first_half = sum(mood_scores[mid:]) / len(mood_scores[mid:])
            second_half = sum(mood_scores[:mid]) / len(mood_scores[:mid])
            if second_half > first_half + 0.5:
                trend = 'improving'
            elif second_half < first_half - 0.5:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'neutral'

        daily_scores = {}
        for entry in entries:
            daily_scores.setdefault(entry['date'], []).append(entry['mood_score'])
        daily_averages = {date: sum(scores) / len(scores) for date, scores in daily_scores.items()}

        return {
            'average_mood_score': round(avg_score, 2),
            'mood_distribution': dict(mood_counts),
            'trend': trend,
            'entries_count': len(entries),
            'daily_averages': daily_averages,
            'dominant_mood': mood_counts.most_common(1)[0][0] if mood_counts else 'neutral',
        }

    def get_writing_streak(self) -> dict:
        if self.use_database:
            entries = self._query_entries_db(start_date=None, end_date=None, mood=None, limit=1000)
        else:
            entries = self._read_entries_file()

        if not entries:
            return {'current_streak': 0, 'longest_streak': 0, 'total_entries': 0}

        dates = sorted({entry['date'] for entry in entries}, reverse=True)
        current_streak = 0
        today = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        if dates and (dates[0] == today or dates[0] == yesterday):
            current_streak = 1
            anchor = datetime.strptime(dates[0], '%Y-%m-%d')
            for offset in range(1, len(dates)):
                expected = (anchor - timedelta(days=offset)).strftime('%Y-%m-%d')
                if offset < len(dates) and dates[offset] == expected:
                    current_streak += 1
                else:
                    break

        return {
            'current_streak': current_streak,
            'total_entries': len(entries),
            'unique_days': len(dates),
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _analyze_sentiment(self, text: str) -> str:
        positive_words = ['happy', 'great', 'good', 'amazing', 'wonderful', 'love', 'excited', 'grateful', 'blessed', 'joy']
        negative_words = ['sad', 'angry', 'stressed', 'worried', 'anxious', 'tired', 'frustrated', 'upset', 'fear', 'hate']

        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            return 'positive'
        if negative_count > positive_count:
            return 'negative'
        return 'neutral'


# Singleton accessor -----------------------------------------------------
_journal_manager: Optional[JournalManager] = None


def get_journal_manager() -> JournalManager:
    global _journal_manager
    if _journal_manager is None:
        _journal_manager = JournalManager()
    return _journal_manager
