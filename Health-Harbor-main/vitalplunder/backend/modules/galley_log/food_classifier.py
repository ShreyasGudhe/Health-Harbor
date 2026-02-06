"""
Galley Log - Food Classifier
============================
Module 6: Diet & Nutrition Tracker

Simple food classification for meal tracking.
Uses a placeholder classifier (can be extended to CNN).

Author: VitalPlunder Team
"""

import os
import json
import numpy as np
from PIL import Image
import io


class FoodClassifier:
    """
    Food Image Classification Engine
    
    Classifies food images into categories and maps to nutrition data.
    
    NOTE: This is a simplified placeholder implementation.
    For production, integrate with a trained CNN model or
    use cloud vision APIs (Google Vision, AWS Rekognition, etc.)
    """
    
    # Supported food categories with example keywords
    FOOD_CATEGORIES = {
        'salad': {
            'keywords': ['salad', 'lettuce', 'greens', 'vegetables'],
            'emoji': '🥗',
            'typical_portion': '200g'
        },
        'sandwich': {
            'keywords': ['sandwich', 'burger', 'bread', 'wrap'],
            'emoji': '🥪',
            'typical_portion': '150g'
        },
        'pizza': {
            'keywords': ['pizza', 'slice'],
            'emoji': '🍕',
            'typical_portion': '1 slice (100g)'
        },
        'pasta': {
            'keywords': ['pasta', 'spaghetti', 'noodles', 'macaroni'],
            'emoji': '🍝',
            'typical_portion': '200g'
        },
        'rice_dish': {
            'keywords': ['rice', 'biryani', 'fried rice', 'pilaf'],
            'emoji': '🍚',
            'typical_portion': '200g'
        },
        'chicken': {
            'keywords': ['chicken', 'poultry', 'wings', 'breast'],
            'emoji': '🍗',
            'typical_portion': '150g'
        },
        'fish': {
            'keywords': ['fish', 'salmon', 'tuna', 'seafood'],
            'emoji': '🐟',
            'typical_portion': '150g'
        },
        'soup': {
            'keywords': ['soup', 'broth', 'stew'],
            'emoji': '🍲',
            'typical_portion': '250ml'
        },
        'fruit': {
            'keywords': ['fruit', 'apple', 'banana', 'orange', 'berries'],
            'emoji': '🍎',
            'typical_portion': '150g'
        },
        'dessert': {
            'keywords': ['cake', 'ice cream', 'dessert', 'cookie', 'chocolate'],
            'emoji': '🍰',
            'typical_portion': '100g'
        },
        'beverage': {
            'keywords': ['coffee', 'tea', 'juice', 'smoothie', 'drink'],
            'emoji': '☕',
            'typical_portion': '250ml'
        },
        'breakfast': {
            'keywords': ['eggs', 'bacon', 'pancake', 'oatmeal', 'cereal'],
            'emoji': '🍳',
            'typical_portion': '200g'
        },
        'snack': {
            'keywords': ['chips', 'nuts', 'snack', 'crackers'],
            'emoji': '🥜',
            'typical_portion': '50g'
        },
        'unknown': {
            'keywords': [],
            'emoji': '🍽️',
            'typical_portion': '150g'
        }
    }
    
    def __init__(self):
        """Initialize the food classifier"""
        self.categories = list(self.FOOD_CATEGORIES.keys())
    
    def classify_by_name(self, food_name):
        """
        Classify food by name using keyword matching
        
        Args:
            food_name: Name or description of the food
            
        Returns:
            Classified food category
        """
        if not food_name:
            return self._get_category_info('unknown')
        
        food_name_lower = food_name.lower()
        
        # Check each category's keywords
        for category, info in self.FOOD_CATEGORIES.items():
            for keyword in info['keywords']:
                if keyword in food_name_lower:
                    return self._get_category_info(category, food_name)
        
        # Default to unknown
        return self._get_category_info('unknown', food_name)
    
    def classify_image(self, image_data):
        """
        Classify food from image
        
        Args:
            image_data: Image bytes or PIL Image
            
        Returns:
            Classification result
            
        NOTE: This is a placeholder implementation.
        In production, use a trained CNN model.
        """
        # Placeholder: Analyze image properties for demo
        try:
            if isinstance(image_data, bytes):
                image = Image.open(io.BytesIO(image_data))
            else:
                image = image_data
            
            # Get image statistics (placeholder analysis)
            width, height = image.size
            
            # For demo, return a random category with confidence
            # In production, this would run the actual CNN model
            np.random.seed(width * height % 1000)
            category_idx = np.random.randint(0, len(self.categories) - 1)
            category = self.categories[category_idx]
            confidence = np.random.uniform(0.6, 0.95)
            
            result = self._get_category_info(category)
            result['classification'] = {
                'confidence': round(confidence * 100, 1),
                'method': 'image_analysis',
                'image_size': f'{width}x{height}'
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Image classification failed: {str(e)}'
            }
    
    def _get_category_info(self, category, food_name=None):
        """Get full category information"""
        info = self.FOOD_CATEGORIES.get(category, self.FOOD_CATEGORIES['unknown'])
        
        return {
            'success': True,
            'category': category,
            'display_name': food_name or category.replace('_', ' ').title(),
            'emoji': info['emoji'],
            'typical_portion': info['typical_portion']
        }


# Create singleton instance
food_classifier = FoodClassifier()


def classify_food_by_name(food_name):
    """Convenience function for name-based classification"""
    return food_classifier.classify_by_name(food_name)


def classify_food_image(image_data):
    """Convenience function for image-based classification"""
    return food_classifier.classify_image(image_data)
