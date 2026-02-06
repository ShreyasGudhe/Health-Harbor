"""
Night Watch - API Routes
========================
Module 5: Sleep Quality Analyzer

REST API endpoints for sleep quality analysis.

Author: VitalPlunder Team
"""

from flask import Blueprint, request, jsonify
from .sleep_analyzer import analyze_sleep, calculate_ideal_bedtime, get_sleep_cycles
from .sleep_model import predict_sleep_quality

# Create Blueprint
night_watch_bp = Blueprint('night_watch', __name__)


@night_watch_bp.route('/', methods=['GET'])
def index():
    """Module info endpoint"""
    return jsonify({
        'module': 'Night Watch',
        'description': 'Sleep Quality Analyzer - Track and improve your sleep',
        'endpoints': {
            'POST /analyze': 'Comprehensive sleep analysis',
            'POST /predict': 'Quick sleep quality prediction',
            'GET /ideal-bedtime': 'Calculate ideal bedtime',
            'GET /sleep-cycles': 'Get optimal wake times'
        }
    })


@night_watch_bp.route('/analyze', methods=['POST'])
def analyze():
    """
    Comprehensive sleep analysis
    
    Request Body:
    {
        "sleep_hours": 7.5,
        "bedtime": "23:00",
        "wake_time": "06:30",
        "consistency_score": 70,
        "caffeine_hours_before": 8,
        "screen_hours_before": 0.5,
        "exercise_today": 1
    }
    
    Returns:
        JSON with quality score, issues, and recommendations
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Please provide sleep data',
                'example': {
                    'sleep_hours': 7.5,
                    'bedtime': '23:00',
                    'wake_time': '06:30'
                }
            }), 400
        
        # Set defaults
        sleep_data = {
            'sleep_hours': data.get('sleep_hours', 7),
            'bedtime': data.get('bedtime', '23:00'),
            'wake_time': data.get('wake_time', '07:00'),
            'consistency_score': data.get('consistency_score', 50),
            'caffeine_hours_before': data.get('caffeine_hours_before', 6),
            'screen_hours_before': data.get('screen_hours_before', 1),
            'exercise_today': 1 if data.get('exercise_today', False) else 0
        }
        
        result = analyze_sleep(sleep_data)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500


@night_watch_bp.route('/predict', methods=['POST'])
def predict():
    """
    Quick sleep quality prediction
    
    Request Body: Same as /analyze
    
    Returns:
        JSON with quality score
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Please provide sleep data'
            }), 400
        
        result = predict_sleep_quality(data)
        result['success'] = True
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Prediction failed: {str(e)}'
        }), 500


@night_watch_bp.route('/ideal-bedtime', methods=['GET'])
def ideal_bedtime():
    """
    Calculate ideal bedtime for desired wake time
    
    Query Params:
        wake_time: Desired wake time (HH:MM format)
        target_hours: Target sleep hours (default: 8)
        
    Returns:
        JSON with ideal bedtime
    """
    wake_time = request.args.get('wake_time', '07:00')
    target_hours = float(request.args.get('target_hours', 8))
    
    result = calculate_ideal_bedtime(wake_time, target_hours)
    
    return jsonify(result), 200 if result['success'] else 400


@night_watch_bp.route('/sleep-cycles', methods=['GET'])
def sleep_cycles():
    """
    Get optimal wake times based on sleep cycles
    
    Query Params:
        bedtime: Planned bedtime (HH:MM format)
        cycles: Number of cycles to calculate (default: 6)
        
    Returns:
        JSON with optimal wake times
    """
    bedtime = request.args.get('bedtime', '23:00')
    cycles = int(request.args.get('cycles', 6))
    
    result = get_sleep_cycles(bedtime, cycles)
    
    return jsonify(result), 200 if result['success'] else 400


@night_watch_bp.route('/sleep-template', methods=['GET'])
def sleep_template():
    """
    Get sleep tracking template
    
    Returns:
        JSON with sleep input fields
    """
    return jsonify({
        'success': True,
        'template': {
            'sleep_hours': {
                'type': 'number',
                'label': 'Hours of Sleep',
                'min': 0,
                'max': 24,
                'step': 0.5,
                'icon': '😴'
            },
            'bedtime': {
                'type': 'time',
                'label': 'Bedtime',
                'icon': '🌙'
            },
            'wake_time': {
                'type': 'time',
                'label': 'Wake Time',
                'icon': '☀️'
            },
            'consistency_score': {
                'type': 'slider',
                'label': 'Schedule Consistency',
                'min': 0,
                'max': 100,
                'description': 'How consistent is your sleep schedule?'
            },
            'caffeine_hours_before': {
                'type': 'number',
                'label': 'Hours Since Last Caffeine',
                'min': 0,
                'max': 24,
                'icon': '☕'
            },
            'screen_hours_before': {
                'type': 'number',
                'label': 'Screen Time Before Bed (hours)',
                'min': 0,
                'max': 6,
                'icon': '📱'
            },
            'exercise_today': {
                'type': 'boolean',
                'label': 'Did You Exercise Today?',
                'icon': '🏃'
            }
        },
        'quality_levels': [
            {'code': 'smooth_sailing', 'label': 'Smooth Sailing', 'range': '80-100'},
            {'code': 'calm_waters', 'label': 'Calm Waters', 'range': '60-79'},
            {'code': 'choppy_seas', 'label': 'Choppy Seas', 'range': '40-59'},
            {'code': 'stormy_night', 'label': 'Stormy Night', 'range': '0-39'}
        ]
    }), 200
