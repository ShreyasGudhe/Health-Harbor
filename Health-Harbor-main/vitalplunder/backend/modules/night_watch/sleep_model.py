"""
Night Watch - Sleep Model
=========================
Module 5: Sleep Quality Analyzer

This module uses regression to predict sleep quality scores
based on sleep patterns and habits.

Author: VitalPlunder Team
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import joblib


class SleepModel:
    """
    Sleep Quality Prediction Model
    
    Analyzes sleep patterns and predicts quality scores.
    """
    
    def __init__(self):
        """Initialize the sleep model"""
        self.model = None
        self.scaler = StandardScaler()
        self._create_default_model()
    
    def _create_default_model(self):
        """
        Create a default regression model for sleep quality
        """
        np.random.seed(42)
        n_samples = 800
        
        # Generate synthetic sleep data
        # Features: sleep_hours, bedtime_hour, wake_hour, consistency_score, 
        #           caffeine_hours_before, screen_hours_before, exercise_today
        
        sleep_hours = np.random.uniform(4, 10, n_samples)
        bedtime_hour = np.random.uniform(20, 26, n_samples) % 24  # 8 PM to 2 AM
        wake_hour = np.random.uniform(5, 11, n_samples)
        consistency_score = np.random.uniform(0, 100, n_samples)
        caffeine_hours = np.random.uniform(0, 12, n_samples)
        screen_hours = np.random.uniform(0, 4, n_samples)
        exercise_today = np.random.choice([0, 1], n_samples, p=[0.4, 0.6])
        
        X = np.column_stack([
            sleep_hours, bedtime_hour, wake_hour, consistency_score,
            caffeine_hours, screen_hours, exercise_today
        ])
        
        # Generate quality score based on factors
        quality = (
            20 +  # Base score
            np.clip((sleep_hours - 4) * 8, 0, 40) +  # Sleep duration
            np.where((bedtime_hour >= 21) & (bedtime_hour <= 23), 10, 0) +  # Good bedtime
            np.where((bedtime_hour >= 23) | (bedtime_hour <= 2), -5, 0) +  # Late bedtime penalty
            consistency_score * 0.15 +  # Consistency bonus
            np.clip(caffeine_hours * 2, 0, 15) +  # Caffeine timing
            np.where(screen_hours < 1, 5, -screen_hours * 3) +  # Screen time
            exercise_today * 8 +  # Exercise bonus
            np.random.normal(0, 5, n_samples)  # Noise
        )
        
        # Clamp to 0-100
        y = np.clip(quality, 0, 100)
        
        # Scale features and train
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = RandomForestRegressor(
            n_estimators=50,
            max_depth=8,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_scaled, y)
    
    def predict_quality(self, sleep_data):
        """
        Predict sleep quality score
        
        Args:
            sleep_data: Dictionary with:
                - sleep_hours: Hours of sleep
                - bedtime: Bedtime string (HH:MM) or hour
                - wake_time: Wake time string (HH:MM) or hour
                - consistency_score: Schedule consistency (0-100)
                - caffeine_hours_before: Hours since last caffeine
                - screen_hours_before: Screen time before bed
                - exercise_today: Whether exercised (0/1)
                
        Returns:
            Sleep quality prediction
        """
        # Parse times
        bedtime_hour = self._parse_time(sleep_data.get('bedtime', '23:00'))
        wake_hour = self._parse_time(sleep_data.get('wake_time', '07:00'))
        
        features = np.array([
            sleep_data.get('sleep_hours', 7),
            bedtime_hour,
            wake_hour,
            sleep_data.get('consistency_score', 50),
            sleep_data.get('caffeine_hours_before', 6),
            sleep_data.get('screen_hours_before', 1),
            sleep_data.get('exercise_today', 0)
        ]).reshape(1, -1)
        
        # Scale and predict
        features_scaled = self.scaler.transform(features)
        quality_score = self.model.predict(features_scaled)[0]
        quality_score = max(0, min(100, quality_score))
        
        # Get quality level
        quality_level = self._get_quality_level(quality_score)
        
        return {
            'quality_score': round(quality_score, 1),
            'quality_level': quality_level,
            'factors': {
                'sleep_duration': sleep_data.get('sleep_hours', 7),
                'bedtime': sleep_data.get('bedtime', '23:00'),
                'wake_time': sleep_data.get('wake_time', '07:00')
            }
        }
    
    def _parse_time(self, time_input):
        """Parse time input to hour float"""
        if isinstance(time_input, (int, float)):
            return float(time_input)
        
        try:
            if ':' in str(time_input):
                parts = str(time_input).split(':')
                return int(parts[0]) + int(parts[1]) / 60
        except:
            pass
        
        return 23.0  # Default
    
    def _get_quality_level(self, score):
        """
        Convert score to pirate-themed quality level
        
        Args:
            score: Quality score (0-100)
            
        Returns:
            Quality level dictionary
        """
        if score >= 80:
            return {
                'code': 'smooth_sailing',
                'label': 'Smooth Sailing',
                'emoji': '⚓',
                'description': 'Excellent sleep! Your night watch was successful.',
                'color': '#10B981'
            }
        elif score >= 60:
            return {
                'code': 'calm_waters',
                'label': 'Calm Waters',
                'emoji': '🌙',
                'description': 'Good sleep quality. Minor improvements possible.',
                'color': '#3B82F6'
            }
        elif score >= 40:
            return {
                'code': 'choppy_seas',
                'label': 'Choppy Seas',
                'emoji': '🌊',
                'description': 'Moderate sleep quality. Focus on improvement.',
                'color': '#F59E0B'
            }
        else:
            return {
                'code': 'stormy_night',
                'label': 'Stormy Night',
                'emoji': '⛈️',
                'description': 'Poor sleep quality. Review your sleep habits.',
                'color': '#EF4444'
            }


# Create singleton instance
sleep_model = SleepModel()


def predict_sleep_quality(sleep_data):
    """Convenience function for sleep quality prediction"""
    return sleep_model.predict_quality(sleep_data)
