"""
Mind Compass - API Routes
=========================
Module 2: Mental Health & Stress Monitor

REST API endpoints for mental health and stress monitoring.

Author: VitalPlunder Team
"""

from flask import Blueprint, request, jsonify
from .stress_predictor import predict_stress_level, get_coping_technique, get_all_coping_techniques, stress_predictor

# Create Blueprint
mind_compass_bp = Blueprint('mind_compass', __name__)


@mind_compass_bp.route('/', methods=['GET'])
def index():
    """Module info endpoint"""
    return jsonify({
        'module': 'Mind Compass',
        'description': 'Mental Health & Stress Monitor - Track your emotional wellbeing',
        'endpoints': {
            'POST /analyze-text': 'Analyze mood from text input',
            'POST /analyze-questionnaire': 'Analyze mood from questionnaire',
            'GET /coping-techniques': 'Get available coping techniques',
            'GET /check-in-template': 'Get mood check-in template'
        }
    })


@mind_compass_bp.route('/analyze-text', methods=['POST'])
def analyze_text():
    """
    Analyze mood and stress from text input
    
    Request Body:
    {
        "text": "I've been feeling really stressed about work lately..."
    }
    
    Returns:
        JSON with stress analysis and recommendations
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Please provide text to analyze',
                'example': {'text': 'Describe how you are feeling...'}
            }), 400
        
        text = data['text']
        
        if len(text.strip()) < 5:
            return jsonify({
                'success': False,
                'error': 'Please provide more detail about how you\'re feeling'
            }), 400
        
        if len(text) > 5000:
            return jsonify({
                'success': False,
                'error': 'Text too long. Please limit to 5000 characters'
            }), 400
        
        # Get analysis
        result = predict_stress_level(text, input_type='text')
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500


@mind_compass_bp.route('/analyze-questionnaire', methods=['POST'])
def analyze_questionnaire():
    """
    Analyze mood from questionnaire responses
    
    Request Body:
    {
        "sleep_quality": 7,
        "energy_level": 6,
        "mood_rating": 7,
        "anxiety_level": 4,
        "social_interaction": 6,
        "work_stress": 5,
        "physical_activity": 5
    }
    
    All values should be 1-10 scale.
    
    Returns:
        JSON with stress analysis and recommendations
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Please provide questionnaire responses'
            }), 400
        
        # Validate required fields
        required = ['mood_rating', 'anxiety_level']
        missing = [f for f in required if f not in data]
        
        if missing:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing)}',
                'required_fields': required,
                'optional_fields': ['sleep_quality', 'energy_level', 'social_interaction', 
                                   'work_stress', 'physical_activity']
            }), 400
        
        # Validate value ranges
        for key, value in data.items():
            if not isinstance(value, (int, float)) or value < 1 or value > 10:
                return jsonify({
                    'success': False,
                    'error': f'Field {key} must be a number between 1 and 10'
                }), 400
        
        # Get analysis
        result = predict_stress_level(data, input_type='questionnaire')
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500


@mind_compass_bp.route('/coping-techniques', methods=['GET'])
def coping_techniques():
    """
    Get all available coping techniques
    
    Query Params:
        technique: Optional specific technique name
        
    Returns:
        JSON with coping techniques
    """
    technique_name = request.args.get('technique')
    
    if technique_name:
        technique = get_coping_technique(technique_name)
        if technique:
            return jsonify({
                'success': True,
                'technique': technique
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Technique "{technique_name}" not found',
                'available': list(get_all_coping_techniques().keys())
            }), 404
    
    return jsonify({
        'success': True,
        'techniques': get_all_coping_techniques()
    }), 200


@mind_compass_bp.route('/check-in-template', methods=['GET'])
def check_in_template():
    """
    Get mood check-in template for frontend
    
    Returns:
        JSON with check-in form template
    """
    template = stress_predictor.get_mood_history_template()
    
    return jsonify({
        'success': True,
        'template': template,
        'instructions': 'Use daily_check_in for detailed tracking, quick_check for fast mood logging'
    }), 200


@mind_compass_bp.route('/stress-levels', methods=['GET'])
def stress_levels():
    """
    Get information about stress levels
    
    Returns:
        JSON with stress level definitions
    """
    return jsonify({
        'success': True,
        'stress_levels': [
            {
                'code': 'steady',
                'label': 'Steady',
                'emoji': '⚓',
                'description': 'Your mental compass is steady',
                'score_range': '0-33',
                'color': '#10B981'
            },
            {
                'code': 'drifting',
                'label': 'Drifting',
                'emoji': '🧭',
                'description': 'Your compass is drifting',
                'score_range': '34-66',
                'color': '#F59E0B'
            },
            {
                'code': 'overboard',
                'label': 'Overboard',
                'emoji': '🆘',
                'description': 'Mind overboard - seek support',
                'score_range': '67-100',
                'color': '#EF4444'
            }
        ],
        'disclaimer': 'This tool is for informational purposes only and is not a substitute for professional mental health care.'
    }), 200
