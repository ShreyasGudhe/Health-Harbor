"""
Storm Watch - API Routes
========================
Module 1: Health Risk Scanner

REST API endpoints for health risk prediction.

Author: VitalPlunder Team
"""

from flask import Blueprint, request, jsonify
from .predict import predict_health_risk, get_risk_factors

# Create Blueprint for this module
storm_watch_bp = Blueprint('storm_watch', __name__)


@storm_watch_bp.route('/', methods=['GET'])
def index():
    """
    Module info endpoint
    """
    return jsonify({
        'module': 'Storm Watch',
        'description': 'Health Risk Scanner - Predict health risk levels',
        'endpoints': {
            'POST /predict': 'Predict health risk based on user metrics',
            'POST /analyze': 'Get detailed risk factor analysis',
            'GET /info': 'Get information about risk levels'
        }
    })


@storm_watch_bp.route('/predict', methods=['POST'])
def predict():
    """
    Predict health risk level
    
    Request Body:
    {
        "age": 35,
        "gender": "male",
        "bmi": 24.5,
        "activity_level": "moderate",
        "diet_quality": "good",
        "sleep_hours": 7,
        "smoking": 0,
        "alcohol_weekly": 3,
        "stress_level": 5,
        "family_history": 0
    }
    
    Returns:
        JSON with risk prediction and advice
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided. Please send health metrics in JSON format.'
            }), 400
        
        # Validate required fields
        required_fields = ['age', 'gender', 'bmi', 'activity_level', 'diet_quality', 'sleep_hours']
        missing_fields = [f for f in required_fields if f not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'required_fields': required_fields
            }), 400
        
        # Validate data types and ranges
        validation_errors = []
        
        if not isinstance(data.get('age'), (int, float)) or data['age'] < 1 or data['age'] > 120:
            validation_errors.append('Age must be between 1 and 120')
        
        if data.get('gender', '').lower() not in ['male', 'female']:
            validation_errors.append('Gender must be "male" or "female"')
        
        if not isinstance(data.get('bmi'), (int, float)) or data['bmi'] < 10 or data['bmi'] > 60:
            validation_errors.append('BMI must be between 10 and 60')
        
        valid_activity = ['sedentary', 'light', 'moderate', 'active', 'very_active']
        if data.get('activity_level', '').lower() not in valid_activity:
            validation_errors.append(f'Activity level must be one of: {", ".join(valid_activity)}')
        
        valid_diet = ['poor', 'fair', 'good', 'excellent']
        if data.get('diet_quality', '').lower() not in valid_diet:
            validation_errors.append(f'Diet quality must be one of: {", ".join(valid_diet)}')
        
        if validation_errors:
            return jsonify({
                'success': False,
                'error': 'Validation failed',
                'details': validation_errors
            }), 400
        
        # Set default values for optional fields
        data.setdefault('smoking', 0)
        data.setdefault('alcohol_weekly', 0)
        data.setdefault('stress_level', 5)
        data.setdefault('family_history', 0)
        
        # Make prediction
        result = predict_health_risk(data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@storm_watch_bp.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze risk factors for user
    
    Request Body: Same as /predict
    
    Returns:
        JSON with detailed risk factor analysis
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Get risk factors
        risk_factors = get_risk_factors(data)
        
        # Also get prediction
        prediction = predict_health_risk(data)
        
        return jsonify({
            'success': True,
            'risk_factors': risk_factors,
            'risk_factor_count': len(risk_factors),
            'prediction_summary': prediction.get('prediction', {}),
            'overall_assessment': 'High priority attention needed' if len(risk_factors) >= 3 
                                 else 'Some areas need attention' if len(risk_factors) >= 1 
                                 else 'Looking good, Captain!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500


@storm_watch_bp.route('/info', methods=['GET'])
def risk_info():
    """
    Get information about risk levels
    """
    return jsonify({
        'success': True,
        'risk_levels': [
            {
                'code': 'calm_seas',
                'label': 'Calm Seas',
                'emoji': '🌊',
                'description': 'Low health risk - smooth sailing ahead',
                'color': '#10B981'  # Green
            },
            {
                'code': 'rising_storm',
                'label': 'Rising Storm',
                'emoji': '⛈️',
                'description': 'Moderate health risk - adjustments recommended',
                'color': '#F59E0B'  # Yellow/Orange
            },
            {
                'code': 'high_alert',
                'label': 'High Alert',
                'emoji': '🚨',
                'description': 'High health risk - immediate attention needed',
                'color': '#EF4444'  # Red
            }
        ],
        'input_parameters': {
            'age': {'type': 'integer', 'range': '1-120', 'required': True},
            'gender': {'type': 'string', 'options': ['male', 'female'], 'required': True},
            'bmi': {'type': 'float', 'range': '10-60', 'required': True},
            'activity_level': {'type': 'string', 'options': ['sedentary', 'light', 'moderate', 'active', 'very_active'], 'required': True},
            'diet_quality': {'type': 'string', 'options': ['poor', 'fair', 'good', 'excellent'], 'required': True},
            'sleep_hours': {'type': 'float', 'range': '0-24', 'required': True},
            'smoking': {'type': 'integer', 'options': [0, 1], 'required': False, 'default': 0},
            'alcohol_weekly': {'type': 'integer', 'range': '0-50', 'required': False, 'default': 0},
            'stress_level': {'type': 'integer', 'range': '1-10', 'required': False, 'default': 5},
            'family_history': {'type': 'integer', 'options': [0, 1], 'required': False, 'default': 0}
        }
    })
