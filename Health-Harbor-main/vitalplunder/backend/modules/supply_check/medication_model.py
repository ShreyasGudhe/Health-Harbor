"""
Supply Check - Medication Model
===============================
Module 4: Medication Adherence Predictor

This module uses classification to predict missed medication doses
based on user history and schedule patterns.

Author: VitalPlunder Team
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import joblib


class MedicationModel:
    """
    Medication Adherence Prediction Model
    
    Predicts the likelihood of missing a medication dose based on
    historical patterns and contextual factors.
    """
    
    def __init__(self):
        """Initialize the medication model"""
        self.model = None
        self.scaler = StandardScaler()
        self._create_default_model()
    
    def _create_default_model(self):
        """
        Create a default classification model
        """
        np.random.seed(42)
        
        # Generate synthetic training data
        # Features: hour_of_day, day_of_week, missed_last_7_days, 
        #           consecutive_taken, medication_count, reminder_set
        n_samples = 1000
        
        # Generate features
        X = np.column_stack([
            np.random.randint(0, 24, n_samples),           # hour_of_day
            np.random.randint(0, 7, n_samples),            # day_of_week
            np.random.randint(0, 5, n_samples),            # missed_last_7_days
            np.random.randint(0, 14, n_samples),           # consecutive_taken
            np.random.randint(1, 6, n_samples),            # medication_count
            np.random.choice([0, 1], n_samples, p=[0.3, 0.7])  # reminder_set
        ])
        
        # Generate target (probability of missing based on features)
        miss_prob = (
            0.1 +  # Base probability
            (X[:, 2] * 0.1) +  # More misses recently = higher prob
            (X[:, 4] * 0.05) +  # More meds = harder to track
            ((X[:, 0] > 21) | (X[:, 0] < 6)).astype(float) * 0.15 +  # Late night/early morning
            (X[:, 5] == 0).astype(float) * 0.2 -  # No reminder
            (X[:, 3] * 0.02)  # Streak reduces miss chance
        )
        miss_prob = np.clip(miss_prob, 0.05, 0.95)
        y = (np.random.random(n_samples) < miss_prob).astype(int)
        
        # Scale and train
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = GradientBoostingClassifier(
            n_estimators=50,
            max_depth=4,
            random_state=42
        )
        self.model.fit(X_scaled, y)
    
    def predict_adherence(self, medication_data):
        """
        Predict medication adherence for upcoming dose
        
        Args:
            medication_data: Dictionary with:
                - hour_of_day: Scheduled hour (0-23)
                - day_of_week: Day of week (0=Mon, 6=Sun)
                - missed_last_7_days: Count of missed doses in past week
                - consecutive_taken: Current streak of doses taken
                - medication_count: Total medications user takes
                - reminder_set: Whether reminder is enabled (0/1)
                
        Returns:
            Adherence prediction with risk level
        """
        # Extract features
        features = np.array([
            medication_data.get('hour_of_day', 8),
            medication_data.get('day_of_week', 0),
            medication_data.get('missed_last_7_days', 0),
            medication_data.get('consecutive_taken', 0),
            medication_data.get('medication_count', 1),
            medication_data.get('reminder_set', 1)
        ]).reshape(1, -1)
        
        # Scale and predict
        features_scaled = self.scaler.transform(features)
        miss_probability = self.model.predict_proba(features_scaled)[0][1]
        adherence_probability = 1 - miss_probability
        
        # Determine risk level
        risk_level = self._get_risk_level(miss_probability)
        
        return {
            'adherence_probability': round(adherence_probability * 100, 1),
            'miss_probability': round(miss_probability * 100, 1),
            'risk_level': risk_level,
            'factors_analyzed': medication_data
        }
    
    def _get_risk_level(self, miss_probability):
        """
        Convert miss probability to pirate-themed risk level
        
        Args:
            miss_probability: Probability of missing dose (0-1)
            
        Returns:
            Risk level dictionary
        """
        if miss_probability <= 0.2:
            return {
                'code': 'stocked',
                'label': 'Supplies Stocked',
                'emoji': '✅',
                'description': 'Good adherence expected. Keep it up!',
                'color': '#10B981'
            }
        elif miss_probability <= 0.5:
            return {
                'code': 'low_supplies',
                'label': 'Low Supplies Warning',
                'emoji': '⚠️',
                'description': 'Moderate risk of missing dose. Stay vigilant!',
                'color': '#F59E0B'
            }
        else:
            return {
                'code': 'critical',
                'label': 'Critical Alert',
                'emoji': '🚨',
                'description': 'High risk of missing dose. Set extra reminders!',
                'color': '#EF4444'
            }
    
    def get_adherence_tips(self, risk_level_code):
        """
        Get tips based on risk level
        
        Args:
            risk_level_code: Risk level code string
            
        Returns:
            List of tips
        """
        tips = {
            'stocked': [
                'Great job maintaining your medication routine!',
                'Consider linking doses to daily habits',
                'Keep medications visible as a reminder'
            ],
            'low_supplies': [
                'Set up phone reminders for each dose',
                'Use a pill organizer to track doses',
                'Ask a family member to help remind you',
                'Consider a medication tracking app'
            ],
            'critical': [
                'Set multiple alarms for this dose',
                'Put medication where you\'ll see it',
                'Ask someone to check in with you',
                'Consider speaking with your pharmacist about adherence strategies',
                'Don\'t skip - consistency is key to effectiveness'
            ]
        }
        return tips.get(risk_level_code, tips['low_supplies'])


# Create singleton instance
medication_model = MedicationModel()


def predict_medication_adherence(medication_data):
    """Convenience function for adherence prediction"""
    result = medication_model.predict_adherence(medication_data)
    result['tips'] = medication_model.get_adherence_tips(result['risk_level']['code'])
    return result
