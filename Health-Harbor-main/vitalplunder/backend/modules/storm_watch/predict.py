"""
Storm Watch - Health Risk Prediction Module
============================================
Module 1: Health Risk Scanner

This module provides prediction functionality for health risk assessment.
It loads the trained model and makes predictions on new user data.

Author: VitalPlunder Team
"""

import os
import joblib
import numpy as np


class HealthRiskPredictor:
    """
    Health Risk Prediction Engine
    
    Predicts health risk levels based on user health metrics.
    Uses a trained Random Forest model.
    """
    
    # Risk level mappings with pirate theme
    RISK_LEVELS = {
        0: {
            'code': 'calm_seas',
            'label': 'Calm Seas',
            'emoji': '🌊',
            'description': 'Smooth sailing ahead! Your health indicators look great.',
            'advice': [
                'Keep up the great work, sailor!',
                'Maintain your current healthy habits.',
                'Consider helping others on their health voyage.'
            ]
        },
        1: {
            'code': 'rising_storm',
            'label': 'Rising Storm',
            'emoji': '⛈️',
            'description': 'Storm clouds gathering. Time to adjust your course.',
            'advice': [
                'Review your diet and exercise routine.',
                'Consider reducing stress levels.',
                'Schedule a check-up with your healthcare provider.',
                'Focus on getting quality sleep.'
            ]
        },
        2: {
            'code': 'high_alert',
            'label': 'High Alert',
            'emoji': '🚨',
            'description': 'Rough waters ahead! Immediate attention recommended.',
            'advice': [
                'Consult with a healthcare professional soon.',
                'Make lifestyle changes a priority.',
                'Track your health metrics daily.',
                'Seek support from family and friends.',
                'Consider professional health coaching.'
            ]
        }
    }
    
    def __init__(self):
        """
        Initialize the predictor by loading the trained model
        """
        self.model_dir = os.path.dirname(os.path.abspath(__file__))
        self.model = None
        self.encoders = None
        self.scaler = None
        self.feature_cols = None
        self._load_model()
    
    def _load_model(self):
        """
        Load the trained model and preprocessing objects
        """
        try:
            self.model = joblib.load(os.path.join(self.model_dir, 'health_risk_model.pkl'))
            self.encoders = joblib.load(os.path.join(self.model_dir, 'encoders.pkl'))
            self.scaler = joblib.load(os.path.join(self.model_dir, 'scaler.pkl'))
            self.feature_cols = joblib.load(os.path.join(self.model_dir, 'feature_cols.pkl'))
            print("✅ Storm Watch model loaded successfully")
        except FileNotFoundError:
            print("⚠️ Model files not found. Please run train_model.py first.")
            self.model = None
    
    def _preprocess_input(self, user_data):
        """
        Preprocess user input for prediction
        
        Args:
            user_data: Dictionary with user health metrics
            
        Returns:
            Preprocessed feature array
        """
        # Create feature array in correct order
        features = []
        
        # Map categorical values
        categorical_mappings = {
            'gender': {'male': 0, 'female': 1},
            'activity_level': {'sedentary': 0, 'light': 1, 'moderate': 2, 'active': 3, 'very_active': 4},
            'diet_quality': {'poor': 0, 'fair': 1, 'good': 2, 'excellent': 3}
        }
        
        for col in self.feature_cols:
            value = user_data.get(col, 0)
            
            # Handle categorical encoding
            if col in categorical_mappings:
                value = categorical_mappings[col].get(str(value).lower(), 0)
            
            features.append(float(value))
        
        # Convert to numpy array and scale
        features = np.array(features).reshape(1, -1)
        features_scaled = self.scaler.transform(features)
        
        return features_scaled
    
    def predict(self, user_data):
        """
        Predict health risk level for user
        
        Args:
            user_data: Dictionary containing:
                - age: int (18-100)
                - gender: str ('male' or 'female')
                - bmi: float (16-50)
                - activity_level: str ('sedentary', 'light', 'moderate', 'active', 'very_active')
                - diet_quality: str ('poor', 'fair', 'good', 'excellent')
                - sleep_hours: float (0-24)
                - smoking: int (0 or 1)
                - alcohol_weekly: int (0-50)
                - stress_level: int (1-10)
                - family_history: int (0 or 1)
                
        Returns:
            Dictionary with prediction results
        """
        if self.model is None:
            return {
                'success': False,
                'error': 'Model not loaded. Please train the model first.',
                'suggestion': 'Run: python train_model.py'
            }
        
        try:
            # Preprocess input
            features = self._preprocess_input(user_data)
            
            # Get prediction and probabilities
            prediction = self.model.predict(features)[0]
            probabilities = self.model.predict_proba(features)[0]
            
            # Get risk level details
            risk_info = self.RISK_LEVELS[prediction]
            
            # Calculate confidence
            confidence = float(max(probabilities)) * 100
            
            # Build response
            result = {
                'success': True,
                'prediction': {
                    'risk_code': risk_info['code'],
                    'risk_label': risk_info['label'],
                    'risk_emoji': risk_info['emoji'],
                    'description': risk_info['description'],
                    'confidence': round(confidence, 1)
                },
                'probabilities': {
                    'calm_seas': round(float(probabilities[0]) * 100, 1),
                    'rising_storm': round(float(probabilities[1]) * 100, 1),
                    'high_alert': round(float(probabilities[2]) * 100, 1)
                },
                'advice': risk_info['advice'],
                'input_summary': {
                    'age': user_data.get('age'),
                    'bmi': user_data.get('bmi'),
                    'activity_level': user_data.get('activity_level'),
                    'sleep_hours': user_data.get('sleep_hours')
                }
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Prediction failed: {str(e)}'
            }
    
    def get_risk_factors(self, user_data):
        """
        Analyze which factors contribute most to the user's risk
        
        Args:
            user_data: Dictionary with user health metrics
            
        Returns:
            List of risk factors with impact levels
        """
        risk_factors = []
        
        # Check BMI
        bmi = user_data.get('bmi', 22)
        if bmi < 18.5:
            risk_factors.append({'factor': 'Underweight BMI', 'impact': 'moderate', 'suggestion': 'Consider consulting a nutritionist'})
        elif bmi >= 25 and bmi < 30:
            risk_factors.append({'factor': 'Overweight BMI', 'impact': 'moderate', 'suggestion': 'Focus on balanced diet and exercise'})
        elif bmi >= 30:
            risk_factors.append({'factor': 'Obese BMI', 'impact': 'high', 'suggestion': 'Consult healthcare provider for weight management plan'})
        
        # Check activity level
        if user_data.get('activity_level', '').lower() == 'sedentary':
            risk_factors.append({'factor': 'Sedentary lifestyle', 'impact': 'high', 'suggestion': 'Aim for at least 30 minutes of activity daily'})
        
        # Check sleep
        sleep = user_data.get('sleep_hours', 7)
        if sleep < 6:
            risk_factors.append({'factor': 'Insufficient sleep', 'impact': 'moderate', 'suggestion': 'Aim for 7-9 hours of sleep'})
        elif sleep > 9:
            risk_factors.append({'factor': 'Excessive sleep', 'impact': 'low', 'suggestion': 'Monitor for underlying conditions'})
        
        # Check smoking
        if user_data.get('smoking', 0) == 1:
            risk_factors.append({'factor': 'Smoking', 'impact': 'high', 'suggestion': 'Consider smoking cessation programs'})
        
        # Check alcohol
        alcohol = user_data.get('alcohol_weekly', 0)
        if alcohol > 14:
            risk_factors.append({'factor': 'High alcohol consumption', 'impact': 'moderate', 'suggestion': 'Limit to moderate drinking levels'})
        
        # Check stress
        stress = user_data.get('stress_level', 5)
        if stress >= 7:
            risk_factors.append({'factor': 'High stress levels', 'impact': 'moderate', 'suggestion': 'Practice stress management techniques'})
        
        # Check diet
        if user_data.get('diet_quality', '').lower() == 'poor':
            risk_factors.append({'factor': 'Poor diet quality', 'impact': 'high', 'suggestion': 'Increase fruits, vegetables, and whole grains'})
        
        return risk_factors


# Create a singleton instance for easy import
predictor = HealthRiskPredictor()


def predict_health_risk(user_data):
    """
    Convenience function for health risk prediction
    
    Args:
        user_data: Dictionary with user health metrics
        
    Returns:
        Prediction result dictionary
    """
    return predictor.predict(user_data)


def get_risk_factors(user_data):
    """
    Convenience function for risk factor analysis
    
    Args:
        user_data: Dictionary with user health metrics
        
    Returns:
        List of risk factors
    """
    return predictor.get_risk_factors(user_data)
