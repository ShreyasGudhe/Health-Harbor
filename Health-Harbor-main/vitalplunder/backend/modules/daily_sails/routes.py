"""
Daily Sails - API Routes
=========================
Habit Tracking endpoints.

Endpoints:
- GET /api/daily-sails/habits - List all habits
- POST /api/daily-sails/habits - Create habit
- POST /api/daily-sails/complete - Complete habit
- POST /api/daily-sails/uncomplete - Uncomplete habit
- DELETE /api/daily-sails/habits/:id - Delete habit
- GET /api/daily-sails/score - Consistency score

Author: VitalPlunder Team
"""

from flask import Blueprint, request, jsonify
from .habit_manager import get_habit_manager, HabitManager

daily_sails_bp = Blueprint('daily_sails', __name__, url_prefix='/api/daily-sails')


@daily_sails_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'module': 'Daily Sails',
        'message': 'Set your sails for success! ⛵'
    })


@daily_sails_bp.route('/habits', methods=['GET'])
def get_habits():
    """
    Get all habits with completion status
    
    Query params:
    - active_only: Filter active habits only (default true)
    """
    try:
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        manager = get_habit_manager()
        habits = manager.get_habits(active_only=active_only)
        
        return jsonify({
            'success': True,
            'count': len(habits),
            'habits': habits
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@daily_sails_bp.route('/habits', methods=['POST'])
def create_habit():
    """
    Create a new habit
    
    Request body:
    {
        "name": "Morning Exercise",
        "category": "fitness",
        "target_days": 5,
        "description": "30 min workout"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'name' not in data or not data['name'].strip():
            return jsonify({'error': 'Habit name is required'}), 400
        
        manager = get_habit_manager()
        habit = manager.create_habit(
            habit_name=data['name'],
            category=data.get('category', 'other'),
            target_days=data.get('target_days', 7),
            description=data.get('description', '')
        )
        
        return jsonify({
            'success': True,
            'habit': habit,
            'message': 'New sail set for your voyage! ⛵'
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@daily_sails_bp.route('/complete', methods=['POST'])
def complete_habit():
    """
    Mark a habit as completed
    
    Request body:
    {
        "habit_id": "123456",
        "date": "2026-01-16"  // optional
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'habit_id' not in data:
            return jsonify({'error': 'habit_id is required'}), 400
        
        manager = get_habit_manager()
        completion = manager.complete_habit(
            habit_id=data['habit_id'],
            date=data.get('date')
        )
        
        return jsonify({
            'success': True,
            'completion': completion,
            'message': 'Sail completed! Keep the momentum! 🌟'
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@daily_sails_bp.route('/uncomplete', methods=['POST'])
def uncomplete_habit():
    """
    Remove completion for a habit
    
    Request body:
    {
        "habit_id": "123456",
        "date": "2026-01-16"  // optional
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'habit_id' not in data:
            return jsonify({'error': 'habit_id is required'}), 400
        
        manager = get_habit_manager()
        manager.uncomplete_habit(
            habit_id=data['habit_id'],
            date=data.get('date')
        )
        
        return jsonify({
            'success': True,
            'message': 'Completion removed'
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@daily_sails_bp.route('/habits/<habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    """Delete a habit"""
    try:
        manager = get_habit_manager()
        manager.delete_habit(habit_id)
        
        return jsonify({
            'success': True,
            'message': 'Habit removed from your voyage'
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@daily_sails_bp.route('/score', methods=['GET'])
def get_score():
    """
    Get habit consistency score
    
    Query params:
    - days: Number of days to analyze (default 30)
    """
    try:
        days = request.args.get('days', 30, type=int)
        
        manager = get_habit_manager()
        score = manager.get_consistency_score(days=days)
        
        return jsonify({
            'success': True,
            'score': score
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@daily_sails_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get available habit categories"""
    return jsonify({
        'success': True,
        'categories': HabitManager.HABIT_CATEGORIES
    })
