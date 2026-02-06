"""
Galley Log - API Routes
=======================
Module 6: Diet & Nutrition Tracker

REST API endpoints for food tracking and nutrition analysis.

Author: VitalPlunder Team
"""

import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from .food_classifier import classify_food_by_name, classify_food_image
from .nutrition_mapper import get_food_nutrition, log_meal, get_daily_summary

# Create Blueprint
galley_log_bp = Blueprint('galley_log', __name__)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@galley_log_bp.route('/', methods=['GET'])
def index():
    """Module info endpoint"""
    return jsonify({
        'module': 'Galley Log',
        'description': 'Diet & Nutrition Tracker - Track meals and nutrition',
        'endpoints': {
            'POST /classify': 'Classify food by name',
            'POST /classify-image': 'Classify food from image',
            'POST /nutrition': 'Get nutrition for food',
            'POST /log-meal': 'Log a complete meal',
            'POST /daily-summary': 'Get daily nutrition summary'
        }
    })


@galley_log_bp.route('/classify', methods=['POST'])
def classify():
    """
    Classify food by name
    
    Request Body:
    {
        "food_name": "chicken salad"
    }
    
    Returns:
        JSON with food classification
    """
    try:
        data = request.get_json()
        
        if not data or 'food_name' not in data:
            return jsonify({
                'success': False,
                'error': 'Please provide food_name'
            }), 400
        
        result = classify_food_by_name(data['food_name'])
        
        # Add nutrition info
        if result['success']:
            nutrition = get_food_nutrition(result['category'], name=result['display_name'])
            result['nutrition'] = nutrition
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Classification failed: {str(e)}'
        }), 500


@galley_log_bp.route('/classify-image', methods=['POST'])
def classify_image():
    """
    Classify food from uploaded image
    
    Form Data:
        image: Image file
        food_name: Optional name hint
        
    Returns:
        JSON with food classification and nutrition
    """
    try:
        # Check if image was uploaded
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file uploaded'
            }), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Read image data
        image_data = file.read()
        
        # Optional: use food name hint
        food_name = request.form.get('food_name')
        
        if food_name:
            # If name provided, use name-based classification
            result = classify_food_by_name(food_name)
        else:
            # Use image classification
            result = classify_food_image(image_data)
        
        # Add nutrition info
        if result.get('success'):
            nutrition = get_food_nutrition(result['category'], name=result.get('display_name'))
            result['nutrition'] = nutrition
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Image classification failed: {str(e)}'
        }), 500


@galley_log_bp.route('/nutrition', methods=['POST'])
def nutrition():
    """
    Get nutrition information for food
    
    Request Body:
    {
        "food_category": "chicken",
        "portion_multiplier": 1.5,
        "name": "Grilled Chicken Breast"
    }
    
    Returns:
        JSON with nutrition information
    """
    try:
        data = request.get_json()
        
        if not data or 'food_category' not in data:
            return jsonify({
                'success': False,
                'error': 'Please provide food_category'
            }), 400
        
        category = data['food_category']
        portion = data.get('portion_multiplier', 1.0)
        name = data.get('name')
        
        nutrition_info = get_food_nutrition(category, portion, name)
        
        return jsonify({
            'success': True,
            'nutrition': nutrition_info
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get nutrition: {str(e)}'
        }), 500


@galley_log_bp.route('/log-meal', methods=['POST'])
def log_meal_endpoint():
    """
    Log a complete meal
    
    Request Body:
    {
        "items": [
            {
                "name": "Grilled Chicken",
                "category": "chicken",
                "portion_multiplier": 1.0
            },
            {
                "name": "Rice",
                "category": "rice",
                "portion_multiplier": 1.5
            }
        ],
        "meal_type": "lunch"
    }
    
    Returns:
        JSON with meal summary and nutrition totals
    """
    try:
        data = request.get_json()
        
        if not data or 'items' not in data:
            return jsonify({
                'success': False,
                'error': 'Please provide items array',
                'example': {
                    'items': [
                        {'name': 'Chicken', 'category': 'chicken', 'portion_multiplier': 1.0}
                    ],
                    'meal_type': 'lunch'
                }
            }), 400
        
        items = data['items']
        meal_type = data.get('meal_type', 'meal')
        
        if not isinstance(items, list):
            return jsonify({
                'success': False,
                'error': 'Items must be a list'
            }), 400
        
        result = log_meal(items)
        result['meal_type'] = meal_type
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to log meal: {str(e)}'
        }), 500


@galley_log_bp.route('/daily-summary', methods=['POST'])
def daily_summary():
    """
    Get daily nutrition summary
    
    Request Body:
    {
        "meals": [
            {
                "totals": {"calories": 400, "protein": 30, ...}
            }
        ]
    }
    
    Returns:
        JSON with daily nutrition summary
    """
    try:
        data = request.get_json()
        
        if not data or 'meals' not in data:
            return jsonify({
                'success': False,
                'error': 'Please provide meals array'
            }), 400
        
        meals = data['meals']
        
        result = get_daily_summary(meals)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get summary: {str(e)}'
        }), 500


@galley_log_bp.route('/food-categories', methods=['GET'])
def food_categories():
    """
    Get all available food categories
    
    Returns:
        JSON with food categories and typical nutrition
    """
    from .food_classifier import food_classifier
    from .nutrition_mapper import nutrition_mapper
    
    categories = []
    for category, info in food_classifier.FOOD_CATEGORIES.items():
        if category != 'unknown':
            nutrition = nutrition_mapper.NUTRITION_DB.get(category, {})
            categories.append({
                'category': category,
                'emoji': info['emoji'],
                'typical_portion': info['typical_portion'],
                'sample_calories': nutrition.get('calories', 'N/A')
            })
    
    return jsonify({
        'success': True,
        'categories': categories,
        'count': len(categories)
    }), 200


@galley_log_bp.route('/daily-goals', methods=['GET'])
def daily_goals():
    """
    Get recommended daily nutrition values
    
    Returns:
        JSON with daily recommended values
    """
    from .nutrition_mapper import nutrition_mapper
    
    return jsonify({
        'success': True,
        'recommended_daily': nutrition_mapper.DAILY_VALUES,
        'note': 'Values based on a 2000 calorie diet. Individual needs may vary.'
    }), 200
