"""
Captain's Log - API Routes
===========================
Digital Diary & Mood Tracking endpoints.

Endpoints:
- POST /api/captains-log/add - Add journal entry
- GET /api/captains-log/history - Get journal history
- GET /api/captains-log/mood-trends - Get mood analysis
- GET /api/captains-log/streak - Get writing streak

Author: VitalPlunder Team
"""

from flask import Blueprint, request, jsonify
from .journal_manager import get_journal_manager, JournalManager

captains_log_bp = Blueprint('captains_log', __name__, url_prefix='/api/captains-log')


@captains_log_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'module': "Captain's Log",
        'message': 'Ready to record your journey! 📖'
    })


@captains_log_bp.route('/add', methods=['POST'])
def add_entry():
    """
    Add a new journal entry
    
    Request body:
    {
        "journal_text": "Today was a great day...",
        "mood": "happy",
        "date": "2026-01-16"  // optional
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'journal_text' not in data or not data['journal_text'].strip():
            return jsonify({'error': 'Journal text is required'}), 400
        
        if 'mood' not in data:
            return jsonify({'error': 'Mood is required'}), 400
        
        manager = get_journal_manager()
        entry = manager.add_entry(
            journal_text=data['journal_text'],
            mood=data['mood'],
            date=data.get('date')
        )
        
        return jsonify({
            'success': True,
            'entry': entry,
            'message': "Entry logged in the Captain's Log! 📝"
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@captains_log_bp.route('/history', methods=['GET'])
def get_history():
    """
    Get journal entry history
    
    Query params:
    - start_date: Filter from date
    - end_date: Filter until date
    - mood: Filter by mood
    - limit: Max entries (default 50)
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        mood = request.args.get('mood')
        limit = request.args.get('limit', 50, type=int)
        
        manager = get_journal_manager()
        entries = manager.get_entries(
            start_date=start_date,
            end_date=end_date,
            mood=mood,
            limit=limit
        )
        
        return jsonify({
            'success': True,
            'count': len(entries),
            'entries': entries
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@captains_log_bp.route('/mood-trends', methods=['GET'])
def get_mood_trends():
    """
    Get mood trend analysis
    
    Query params:
    - days: Number of days to analyze (default 30)
    """
    try:
        days = request.args.get('days', 30, type=int)
        
        manager = get_journal_manager()
        trends = manager.get_mood_trends(days=days)
        
        return jsonify({
            'success': True,
            'trends': trends
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@captains_log_bp.route('/streak', methods=['GET'])
def get_streak():
    """Get writing streak information"""
    try:
        manager = get_journal_manager()
        streak = manager.get_writing_streak()
        
        return jsonify({
            'success': True,
            'streak': streak
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@captains_log_bp.route('/moods', methods=['GET'])
def get_moods():
    """Get available mood options"""
    return jsonify({
        'success': True,
        'moods': JournalManager.MOODS,
        'mood_scores': JournalManager.MOOD_SCORES
    })
