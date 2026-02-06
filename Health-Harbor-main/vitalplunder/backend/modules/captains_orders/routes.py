"""
Captain's Orders - API Routes
=============================
Module 3: Lifestyle Coaching Engine

REST API endpoints for lifestyle analysis and coaching.

Author: VitalPlunder Team
"""

from flask import Blueprint, request, jsonify
from .lifestyle_model import analyze_lifestyle, get_lifestyle_score
from .lifestyle_rules import get_recommendations, get_daily_guidance, lifestyle_rules

# Create Blueprint
captains_orders_bp = Blueprint('captains_orders', __name__)


@captains_orders_bp.route('/', methods=['GET'])
def index():
    """Module info endpoint"""
    return jsonify({
        'module': "Captain's Orders",
        'description': 'Lifestyle Coaching Engine - Track and improve daily habits',
        'endpoints': {
            'POST /analyze': 'Analyze daily habits and get lifestyle score',
            'POST /recommendations': 'Get personalized recommendations',
            'GET /daily-orders': 'Get daily guidance',
            'GET /habits-template': 'Get habit tracking template'
        }
    })


@captains_orders_bp.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze daily habits and calculate lifestyle score
    
    Request Body:
    {
        "exercise_mins": 30,
        "screen_hours": 6,
        "sleep_hours": 7.5,
        "steps": 8000,
        "water_glasses": 8
    }
    
    Returns:
        JSON with lifestyle score, breakdown, and profile
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Please provide habit data',
                'example': {
                    'exercise_mins': 30,
                    'screen_hours': 6,
                    'sleep_hours': 7.5,
                    'steps': 8000,
                    'water_glasses': 8
                }
            }), 400
        
        # Validate and set defaults
        habits = {
            'exercise_mins': max(0, data.get('exercise_mins', 0)),
            'screen_hours': max(0, data.get('screen_hours', 0)),
            'sleep_hours': max(0, min(24, data.get('sleep_hours', 7))),
            'steps': max(0, data.get('steps', 0)),
            'water_glasses': max(0, data.get('water_glasses', 0))
        }
        
        # Analyze habits
        result = analyze_lifestyle(habits)
        
        # Add recommendations
        recommendations = get_recommendations(habits)
        result['recommendations'] = recommendations
        
        # Add coaching message
        result['coaching_message'] = lifestyle_rules.generate_coaching_message(
            result['lifestyle_score'],
            result['profile']['name']
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500


@captains_orders_bp.route('/recommendations', methods=['POST'])
def recommendations():
    """
    Get personalized recommendations based on habits
    
    Request Body: Same as /analyze
    
    Returns:
        JSON with prioritized recommendations
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Please provide habit data'
            }), 400
        
        habits = {
            'exercise_mins': max(0, data.get('exercise_mins', 0)),
            'screen_hours': max(0, data.get('screen_hours', 0)),
            'sleep_hours': max(0, min(24, data.get('sleep_hours', 7))),
            'steps': max(0, data.get('steps', 0)),
            'water_glasses': max(0, data.get('water_glasses', 0))
        }
        
        recommendations = get_recommendations(habits)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'count': len(recommendations),
            'summary': 'All systems green!' if not recommendations else 
                      f'{len(recommendations)} area(s) need attention'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get recommendations: {str(e)}'
        }), 500


@captains_orders_bp.route('/daily-orders', methods=['GET'])
def daily_orders():
    """
    Get daily guidance/orders
    
    Query Params:
        time: 'morning', 'afternoon', or 'evening' (default: morning)
        
    Returns:
        JSON with daily guidance
    """
    time_of_day = request.args.get('time', 'morning').lower()
    
    if time_of_day not in ['morning', 'afternoon', 'evening']:
        time_of_day = 'morning'
    
    orders = get_daily_guidance(time_of_day)
    
    return jsonify({
        'success': True,
        'time_of_day': time_of_day,
        'orders': orders
    }), 200


@captains_orders_bp.route('/habits-template', methods=['GET'])
def habits_template():
    """
    Get habit tracking template for frontend
    
    Returns:
        JSON with habit input fields and ranges
    """
    return jsonify({
        'success': True,
        'template': {
            'exercise_mins': {
                'label': 'Exercise (minutes)',
                'type': 'number',
                'min': 0,
                'max': 300,
                'target': 30,
                'unit': 'mins',
                'icon': '🏃'
            },
            'screen_hours': {
                'label': 'Screen Time (hours)',
                'type': 'number',
                'min': 0,
                'max': 24,
                'target': 6,
                'unit': 'hours',
                'icon': '📱'
            },
            'sleep_hours': {
                'label': 'Sleep (hours)',
                'type': 'number',
                'min': 0,
                'max': 24,
                'target': 8,
                'unit': 'hours',
                'icon': '😴'
            },
            'steps': {
                'label': 'Steps',
                'type': 'number',
                'min': 0,
                'max': 50000,
                'target': 8000,
                'unit': 'steps',
                'icon': '👟'
            },
            'water_glasses': {
                'label': 'Water (glasses)',
                'type': 'number',
                'min': 0,
                'max': 20,
                'target': 8,
                'unit': 'glasses',
                'icon': '💧'
            }
        },
        'scoring': {
            'excellent': '80-100',
            'good': '60-79',
            'fair': '40-59',
            'needs_improvement': '0-39'
        }
    }), 200


@captains_orders_bp.route('/weekly-template', methods=['GET'])
def weekly_template():
    """
    Get weekly summary template
    
    Returns:
        JSON with weekly tracking structure
    """
    template = lifestyle_rules.get_weekly_summary_template()
    
    return jsonify({
        'success': True,
        'template': template
    }), 200
