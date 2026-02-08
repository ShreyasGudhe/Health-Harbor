"""SQLAlchemy models for Captain's Log."""

import os

from sqlalchemy import Column, Integer, String, Text

from modules.database import Base

TABLE_NAME = os.getenv('CAPTAINS_LOG_TABLE_NAME', 'captains_log_entries')


class JournalEntry(Base):
    __tablename__ = TABLE_NAME

    id = Column(String(32), primary_key=True)
    date = Column(String(10), nullable=False)  # YYYY-MM-DD
    time = Column(String(8), nullable=False)   # HH:MM
    journal_text = Column(Text, nullable=False)
    mood = Column(String(32), nullable=False)
    mood_score = Column(Integer, nullable=False)
    word_count = Column(Integer, nullable=False)
    created_at = Column(String(40), nullable=False)
    sentiment = Column(String(32), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'time': self.time,
            'journal_text': self.journal_text,
            'mood': self.mood,
            'mood_score': self.mood_score,
            'word_count': self.word_count,
            'created_at': self.created_at,
            'sentiment': self.sentiment
        }

    @staticmethod
    def from_payload(payload):
        return JournalEntry(
            id=payload['id'],
            date=payload['date'],
            time=payload['time'],
            journal_text=payload['journal_text'],
            mood=payload['mood'],
            mood_score=payload['mood_score'],
            word_count=payload['word_count'],
            created_at=payload['created_at'],
            sentiment=payload['sentiment']
        )
