"""
Supply Check - API Routes
=========================
Module 4: Medication Adherence Predictor

REST API endpoints for medication tracking and adherence prediction.

Author: VitalPlunder Team
"""

from flask import Blueprint, request, jsonify
from .medication_model import predict_medication_adherence
from .adherence_predictor import (
    analyze_medication_schedule, 
    get_upcoming_doses, 
    calculate_adherence_score
)

# Create Blueprint
supply_check_bp = Blueprint('supply_check', __name__)


@supply_check_bp.route('/', methods=['GET'])
def index():
    """Module info endpoint"""
    return jsonify({
        'module': 'Supply Check',
        'description': 'Medication Adherence Predictor - Track and predict medication compliance',
        'endpoints': {
            'POST /predict': 'Predict adherence for a single dose',
            'POST /analyze-schedule': 'Analyze full medication schedule',
            'POST /upcoming': 'Get upcoming doses',
            'POST /adherence-score': 'Calculate adherence score from history'
        }
    })


@supply_check_bp.route('/predict', methods=['POST'])
def predict():
    """
    Predict adherence for a single dose
    
    Request Body:
    {
        "hour_of_day": 8,
        "day_of_week": 1,
        "missed_last_7_days": 1,
        "consecutive_taken": 5,
        "medication_count": 2,
        "reminder_set": 1
    }
    
    Returns:
        JSON with adherence prediction and tips
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Please provide medication data'
            }), 400
        
        # Set defaults
        medication_data = {
            'hour_of_day': data.get('hour_of_day', 8),
            'day_of_week': data.get('day_of_week', 0),
            'missed_last_7_days': max(0, data.get('missed_last_7_days', 0)),
            'consecutive_taken': max(0, data.get('consecutive_taken', 0)),
            'medication_count': max(1, data.get('medication_count', 1)),
            'reminder_set': 1 if data.get('reminder_set', True) else 0
        }
        
        result = predict_medication_adherence(medication_data)
        result['success'] = True
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Prediction failed: {str(e)}'
        }), 500


@supply_check_bp.route('/analyze-schedule', methods=['POST'])
def analyze_schedule():
    """
    Analyze a complete medication schedule
    
    Request Body:
    {
        "medications": [
            {
                "name": "Medication A",
                "dosage": "10mg",
                "times": ["08:00", "20:00"],
                "frequency": "daily",
                "missed_last_7_days": 1,
                "consecutive_taken": 5,
                "reminder_set": true
            }
        ]
    }
    
    Returns:
        JSON with schedule analysis and risk assessment
    """
    try:
        data = request.get_json()
        
        if not data or 'medications' not in data:
            return jsonify({
                'success': False,
                'error': 'Please provide medications list',
                'example': {
                    'medications': [
                        {
                            'name': 'Aspirin',
                            'dosage': '100mg',
                            'times': ['08:00'],
                            'frequency': 'daily'
                        }
                    ]
                }
            }), 400
        
        medications = data['medications']
        
        if not isinstance(medications, list):
            return jsonify({
                'success': False,
                'error': 'Medications must be a list'
            }), 400
        
        result = analyze_medication_schedule(medications)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500


@supply_check_bp.route('/upcoming', methods=['POST'])
def upcoming():
    """
    Get upcoming doses within specified time range
    
    Request Body:
    {
        "medications": [...],
        "hours_ahead": 24
    }
    
    Returns:
        JSON with upcoming doses
    """
    try:
        data = request.get_json()
        
        if not data or 'medications' not in data:
            return jsonify({
                'success': False,
                'error': 'Please provide medications list'
            }), 400
        
        medications = data['medications']
        hours_ahead = data.get('hours_ahead', 24)
        
        result = get_upcoming_doses(medications, hours_ahead)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get upcoming doses: {str(e)}'
        }), 500


@supply_check_bp.route('/adherence-score', methods=['POST'])
def adherence_score():
    """
    Calculate adherence score from history
    
    Request Body:
    {
        "history": [
            {"date": "2026-01-15", "medication": "Aspirin", "taken": true},
            {"date": "2026-01-14", "medication": "Aspirin", "taken": true},
            {"date": "2026-01-13", "medication": "Aspirin", "taken": false}
        ]
    }
    
    Returns:
        JSON with adherence score and statistics
    """
    try:
        data = request.get_json()
        
        if not data or 'history' not in data:
            return jsonify({
                'success': False,
                'error': 'Please provide history data'
            }), 400
        
        history = data['history']
        
        if not isinstance(history, list):
            return jsonify({
                'success': False,
                'error': 'History must be a list'
            }), 400
        
        result = calculate_adherence_score(history)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Calculation failed: {str(e)}'
        }), 500


@supply_check_bp.route('/medication-template', methods=['GET'])
def medication_template():
    """
    Get medication entry template
    
    Returns:
        JSON with medication form template
    """
    return jsonify({
        'success': True,
        'template': {
            'name': {
                'type': 'text',
                'label': 'Medication Name',
                'required': True
            },
            'dosage': {
                'type': 'text',
                'label': 'Dosage',
                'placeholder': 'e.g., 10mg, 1 tablet',
                'required': True
            },
            'times': {
                'type': 'time_array',
                'label': 'Scheduled Times',
                'format': 'HH:MM',
                'required': True
            },
            'frequency': {
                'type': 'select',
                'label': 'Frequency',
                'options': ['daily', 'weekly', 'as_needed'],
                'default': 'daily'
            },
            'reminder_set': {
                'type': 'boolean',
                'label': 'Enable Reminders',
                'default': True
            },
            'notes': {
                'type': 'textarea',
                'label': 'Notes',
                'placeholder': 'e.g., Take with food'
            }
        }
    }), 200
