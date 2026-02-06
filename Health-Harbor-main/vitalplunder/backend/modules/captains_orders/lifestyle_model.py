"""
Captain's Orders - Lifestyle Model
==================================
Module 3: Lifestyle Coaching Engine

This module uses KMeans clustering to identify lifestyle patterns
and provide personalized coaching recommendations.

Author: VitalPlunder Team
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib
import os


class LifestyleModel:
    """
    Lifestyle Pattern Analysis using KMeans Clustering
    
    Clusters users into lifestyle profiles and provides
    personalized recommendations.
    """
    
    # Lifestyle cluster profiles
    CLUSTER_PROFILES = {
        0: {
            'name': 'The Anchored Sailor',
            'emoji': '⚓',
            'description': 'Balanced lifestyle with good habits',
            'strengths': ['Good sleep routine', 'Regular activity', 'Balanced screen time'],
            'color': '#10B981'
        },
        1: {
            'name': 'The Night Navigator',
            'emoji': '🌙',
            'description': 'Night owl with room for improvement',
            'strengths': ['Adaptable schedule', 'Creative energy'],
            'color': '#6366F1'
        },
        2: {
            'name': 'The Desk Captain',
            'emoji': '💻',
            'description': 'Sedentary lifestyle, high screen time',
            'strengths': ['Productive work habits', 'Tech savvy'],
            'color': '#F59E0B'
        },
        3: {
            'name': 'The Active Explorer',
            'emoji': '🏃',
            'description': 'High activity but potential burnout risk',
            'strengths': ['Great physical health', 'High energy'],
            'color': '#3B82F6'
        },
        4: {
            'name': 'The Stormy Seas',
            'emoji': '⛈️',
            'description': 'Inconsistent habits needing attention',
            'strengths': ['Room for growth', 'Awareness of issues'],
            'color': '#EF4444'
        }
    }
    
    def __init__(self):
        """Initialize the lifestyle model"""
        self.model = None
        self.scaler = StandardScaler()
        self._create_default_model()
    
    def _create_default_model(self):
        """
        Create a default KMeans model with predefined clusters
        """
        # Generate synthetic training data
        np.random.seed(42)
        n_samples = 500
        
        # Features: exercise_mins, screen_hours, sleep_hours, steps, water_glasses
        # Cluster 0: Balanced (good all around)
        cluster_0 = np.random.normal([45, 4, 7.5, 8000, 8], [15, 1, 0.5, 2000, 2], (100, 5))
        
        # Cluster 1: Night owl (late sleep, moderate activity)
        cluster_1 = np.random.normal([30, 6, 6, 6000, 6], [10, 2, 1, 2000, 2], (100, 5))
        
        # Cluster 2: Sedentary (low activity, high screen)
        cluster_2 = np.random.normal([10, 10, 6.5, 3000, 5], [5, 2, 1, 1000, 2], (100, 5))
        
        # Cluster 3: Very active (high exercise, good habits)
        cluster_3 = np.random.normal([90, 3, 8, 12000, 10], [20, 1, 0.5, 3000, 2], (100, 5))
        
        # Cluster 4: Struggling (low everything)
        cluster_4 = np.random.normal([5, 8, 5, 2000, 3], [5, 2, 1.5, 1000, 1], (100, 5))
        
        # Combine and ensure positive values
        X = np.vstack([cluster_0, cluster_1, cluster_2, cluster_3, cluster_4])
        X = np.clip(X, 0, None)
        
        # Scale and train
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = KMeans(n_clusters=5, random_state=42, n_init=10)
        self.model.fit(X_scaled)
    
    def calculate_lifestyle_score(self, habits):
        """
        Calculate overall lifestyle score (0-100)
        
        Args:
            habits: Dictionary with daily habits
            
        Returns:
            Score and breakdown
        """
        scores = {}
        
        # Exercise score (target: 30-60 mins)
        exercise = habits.get('exercise_mins', 0)
        if exercise >= 30 and exercise <= 90:
            scores['exercise'] = min(100, 50 + exercise)
        elif exercise > 90:
            scores['exercise'] = 90  # Diminishing returns
        else:
            scores['exercise'] = max(0, exercise * 2)
        
        # Screen time score (target: < 6 hours)
        screen = habits.get('screen_hours', 8)
        if screen <= 4:
            scores['screen_time'] = 100
        elif screen <= 6:
            scores['screen_time'] = 80
        elif screen <= 8:
            scores['screen_time'] = 60
        elif screen <= 10:
            scores['screen_time'] = 40
        else:
            scores['screen_time'] = 20
        
        # Sleep score (target: 7-9 hours)
        sleep = habits.get('sleep_hours', 6)
        if sleep >= 7 and sleep <= 9:
            scores['sleep'] = 100
        elif sleep >= 6 and sleep < 7:
            scores['sleep'] = 70
        elif sleep > 9 and sleep <= 10:
            scores['sleep'] = 80
        else:
            scores['sleep'] = max(0, 50 - abs(sleep - 7.5) * 15)
        
        # Steps score (target: 8000-10000)
        steps = habits.get('steps', 0)
        if steps >= 10000:
            scores['steps'] = 100
        elif steps >= 8000:
            scores['steps'] = 90
        elif steps >= 5000:
            scores['steps'] = 70
        elif steps >= 3000:
            scores['steps'] = 50
        else:
            scores['steps'] = max(0, steps / 60)
        
        # Water score (target: 8 glasses)
        water = habits.get('water_glasses', 0)
        scores['hydration'] = min(100, water * 12.5)
        
        # Weighted average
        weights = {
            'exercise': 0.25,
            'screen_time': 0.15,
            'sleep': 0.25,
            'steps': 0.20,
            'hydration': 0.15
        }
        
        total_score = sum(scores[k] * weights[k] for k in weights)
        
        return {
            'total_score': round(total_score, 1),
            'breakdown': {k: round(v, 1) for k, v in scores.items()},
            'grade': self._score_to_grade(total_score)
        }
    
    def _score_to_grade(self, score):
        """Convert score to letter grade"""
        if score >= 90:
            return {'letter': 'A', 'label': 'Excellent', 'emoji': '🏆'}
        elif score >= 80:
            return {'letter': 'B', 'label': 'Good', 'emoji': '⭐'}
        elif score >= 70:
            return {'letter': 'C', 'label': 'Fair', 'emoji': '👍'}
        elif score >= 60:
            return {'letter': 'D', 'label': 'Needs Work', 'emoji': '💪'}
        else:
            return {'letter': 'F', 'label': 'Critical', 'emoji': '🚨'}
    
    def predict_cluster(self, habits):
        """
        Predict lifestyle cluster for user
        
        Args:
            habits: Dictionary with daily habits
            
        Returns:
            Cluster prediction and profile
        """
        # Extract features
        features = np.array([
            habits.get('exercise_mins', 0),
            habits.get('screen_hours', 8),
            habits.get('sleep_hours', 6),
            habits.get('steps', 0),
            habits.get('water_glasses', 4)
        ]).reshape(1, -1)
        
        # Scale and predict
        features_scaled = self.scaler.transform(features)
        cluster = self.model.predict(features_scaled)[0]
        
        # Get profile
        profile = self.CLUSTER_PROFILES.get(cluster, self.CLUSTER_PROFILES[0])
        
        return {
            'cluster_id': int(cluster),
            'profile': profile
        }
    
    def analyze_habits(self, habits):
        """
        Complete habit analysis with scores, clusters, and recommendations
        
        Args:
            habits: Dictionary with daily habits
            
        Returns:
            Complete analysis result
        """
        # Calculate score
        score_result = self.calculate_lifestyle_score(habits)
        
        # Predict cluster
        cluster_result = self.predict_cluster(habits)
        
        return {
            'success': True,
            'lifestyle_score': score_result['total_score'],
            'score_breakdown': score_result['breakdown'],
            'grade': score_result['grade'],
            'profile': cluster_result['profile'],
            'input': habits
        }


# Create singleton instance
lifestyle_model = LifestyleModel()


def analyze_lifestyle(habits):
    """Convenience function for lifestyle analysis"""
    return lifestyle_model.analyze_habits(habits)


def get_lifestyle_score(habits):
    """Get just the lifestyle score"""
    return lifestyle_model.calculate_lifestyle_score(habits)
