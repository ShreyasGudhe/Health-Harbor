"""
Mind Compass - Sentiment Analysis Model
=======================================
Module 2: Mental Health & Stress Monitor

This module provides NLP-based sentiment analysis for mood tracking
and stress level prediction from text inputs.

Uses TextBlob for sentiment analysis with custom stress mapping.

Author: VitalPlunder Team
"""

import os
import json
import pandas as pd
import numpy as np
from textblob import TextBlob
import re


class SentimentAnalyzer:
    """
    Sentiment Analysis Engine for Mental Health Monitoring
    
    Analyzes text input to determine emotional state and stress levels.
    """
    
    # Stress indicators - words that suggest stress/anxiety
    STRESS_INDICATORS = {
        'high_stress': [
            'overwhelmed', 'anxious', 'panic', 'terrified', 'desperate',
            'hopeless', 'exhausted', 'burned out', 'burnout', 'breaking down',
            'cant cope', "can't cope", 'falling apart', 'drowning', 'suffocating',
            'nightmare', 'terrible', 'awful', 'horrible', 'worst', 'crisis'
        ],
        'moderate_stress': [
            'stressed', 'worried', 'nervous', 'tense', 'frustrated',
            'irritated', 'annoyed', 'tired', 'drained', 'struggling',
            'difficult', 'hard time', 'challenging', 'pressure', 'deadline',
            'busy', 'hectic', 'chaos', 'mess', 'confused'
        ],
        'positive': [
            'happy', 'great', 'wonderful', 'amazing', 'excited', 'grateful',
            'blessed', 'peaceful', 'calm', 'relaxed', 'content', 'joyful',
            'optimistic', 'hopeful', 'energized', 'motivated', 'confident',
            'proud', 'accomplished', 'satisfied', 'loved', 'supported'
        ]
    }
    
    # Questionnaire scoring weights
    QUESTIONNAIRE_WEIGHTS = {
        'sleep_quality': 0.15,
        'energy_level': 0.15,
        'mood_rating': 0.20,
        'anxiety_level': 0.20,
        'social_interaction': 0.10,
        'work_stress': 0.15,
        'physical_activity': 0.05
    }
    
    def __init__(self):
        """Initialize the sentiment analyzer"""
        self.stress_keywords = self._compile_keywords()
    
    def _compile_keywords(self):
        """Compile stress keywords into regex patterns for efficient matching"""
        patterns = {}
        for category, words in self.STRESS_INDICATORS.items():
            pattern = '|'.join([re.escape(word) for word in words])
            patterns[category] = re.compile(pattern, re.IGNORECASE)
        return patterns
    
    def analyze_text(self, text):
        """
        Analyze text for sentiment and stress indicators
        
        Args:
            text: User's mood/feeling description
            
        Returns:
            Dictionary with sentiment analysis results
        """
        if not text or not text.strip():
            return {
                'success': False,
                'error': 'Empty text provided'
            }
        
        # Clean text
        cleaned_text = text.strip().lower()
        
        # Get TextBlob sentiment
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 to 1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1
        
        # Count stress indicators
        stress_counts = {
            'high_stress': len(self.stress_keywords['high_stress'].findall(cleaned_text)),
            'moderate_stress': len(self.stress_keywords['moderate_stress'].findall(cleaned_text)),
            'positive': len(self.stress_keywords['positive'].findall(cleaned_text))
        }
        
        # Calculate stress score (0-100, higher = more stressed)
        stress_score = self._calculate_stress_score(polarity, stress_counts)
        
        # Determine stress level
        stress_level = self._get_stress_level(stress_score)
        
        # Get mood category
        mood = self._get_mood_category(polarity, stress_counts)
        
        return {
            'success': True,
            'text_analysis': {
                'polarity': round(polarity, 3),
                'subjectivity': round(subjectivity, 3),
                'stress_indicators': stress_counts
            },
            'stress_score': round(stress_score, 1),
            'stress_level': stress_level,
            'mood': mood,
            'word_count': len(text.split())
        }
    
    def _calculate_stress_score(self, polarity, stress_counts):
        """
        Calculate overall stress score from 0-100
        
        Args:
            polarity: TextBlob polarity (-1 to 1)
            stress_counts: Dictionary of stress indicator counts
            
        Returns:
            Stress score (0-100)
        """
        # Base score from polarity (inverted - negative sentiment = higher stress)
        base_score = (1 - polarity) * 30  # 0-60 range
        
        # Add stress indicator contributions
        base_score += stress_counts['high_stress'] * 15
        base_score += stress_counts['moderate_stress'] * 8
        base_score -= stress_counts['positive'] * 10
        
        # Clamp to 0-100
        return max(0, min(100, base_score))
    
    def _get_stress_level(self, stress_score):
        """
        Convert stress score to pirate-themed stress level
        
        Args:
            stress_score: Numeric score 0-100
            
        Returns:
            Stress level dictionary
        """
        if stress_score <= 33:
            return {
                'code': 'steady',
                'label': 'Steady',
                'emoji': '⚓',
                'description': 'Your mental compass is steady. Keep sailing smoothly!',
                'color': '#10B981'
            }
        elif stress_score <= 66:
            return {
                'code': 'drifting',
                'label': 'Drifting',
                'emoji': '🧭',
                'description': 'Your compass is drifting. Time to recalibrate.',
                'color': '#F59E0B'
            }
        else:
            return {
                'code': 'overboard',
                'label': 'Overboard',
                'emoji': '🆘',
                'description': 'Mind overboard! Seek support and take a break.',
                'color': '#EF4444'
            }
    
    def _get_mood_category(self, polarity, stress_counts):
        """
        Determine mood category based on analysis
        
        Args:
            polarity: Sentiment polarity
            stress_counts: Stress indicator counts
            
        Returns:
            Mood category dictionary
        """
        if stress_counts['high_stress'] > 0:
            return {'category': 'Distressed', 'emoji': '😰'}
        elif stress_counts['positive'] > stress_counts['moderate_stress']:
            if polarity > 0.3:
                return {'category': 'Happy', 'emoji': '😊'}
            else:
                return {'category': 'Content', 'emoji': '🙂'}
        elif stress_counts['moderate_stress'] > 0:
            return {'category': 'Stressed', 'emoji': '😓'}
        elif polarity < -0.2:
            return {'category': 'Down', 'emoji': '😔'}
        elif polarity > 0.2:
            return {'category': 'Positive', 'emoji': '😌'}
        else:
            return {'category': 'Neutral', 'emoji': '😐'}
    
    def analyze_questionnaire(self, responses):
        """
        Analyze questionnaire responses for stress assessment
        
        Args:
            responses: Dictionary with questionnaire answers (1-10 scale)
                - sleep_quality
                - energy_level  
                - mood_rating
                - anxiety_level (inverted - 10 = high anxiety)
                - social_interaction
                - work_stress (inverted - 10 = high stress)
                - physical_activity
                
        Returns:
            Analysis result dictionary
        """
        # Validate responses
        required_fields = ['mood_rating', 'anxiety_level']
        for field in required_fields:
            if field not in responses:
                return {
                    'success': False,
                    'error': f'Missing required field: {field}'
                }
        
        # Calculate weighted score
        total_score = 0
        max_score = 0
        
        for field, weight in self.QUESTIONNAIRE_WEIGHTS.items():
            if field in responses:
                value = responses[field]
                
                # Invert negative indicators
                if field in ['anxiety_level', 'work_stress']:
                    value = 11 - value  # Invert scale
                
                total_score += value * weight
                max_score += 10 * weight
        
        # Normalize to 0-100 (where 100 is best mental state)
        wellness_score = (total_score / max_score) * 100 if max_score > 0 else 50
        
        # Convert to stress score (inverted)
        stress_score = 100 - wellness_score
        
        # Get stress level
        stress_level = self._get_stress_level(stress_score)
        
        return {
            'success': True,
            'wellness_score': round(wellness_score, 1),
            'stress_score': round(stress_score, 1),
            'stress_level': stress_level,
            'responses_analyzed': len(responses),
            'breakdown': {
                'sleep': responses.get('sleep_quality', 'N/A'),
                'energy': responses.get('energy_level', 'N/A'),
                'mood': responses.get('mood_rating', 'N/A'),
                'anxiety': responses.get('anxiety_level', 'N/A')
            }
        }


def generate_stress_dataset(n_samples=500):
    """
    Generate sample stress/mood dataset for reference
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        DataFrame with text samples and stress labels
    """
    np.random.seed(42)
    
    # Sample texts for each stress level
    steady_texts = [
        "Feeling great today, had a wonderful morning walk",
        "Life is good, spending quality time with family",
        "Grateful for another beautiful day",
        "Feeling peaceful and content",
        "Had a productive day at work, feeling accomplished",
        "Enjoying a relaxing evening with a good book",
        "Feeling optimistic about the future",
        "Great workout this morning, feeling energized"
    ]
    
    drifting_texts = [
        "Feeling a bit stressed with work deadlines",
        "Had some challenges today but managing",
        "Feeling tired, need more sleep",
        "Work has been busy lately, feeling the pressure",
        "A bit worried about finances but handling it",
        "Feeling frustrated with traffic today",
        "Having a hard time focusing",
        "Feeling somewhat overwhelmed with responsibilities"
    ]
    
    overboard_texts = [
        "Feeling completely overwhelmed and exhausted",
        "Can't cope with all this stress anymore",
        "Having panic attacks, feeling desperate",
        "Everything feels hopeless right now",
        "Burned out and can't function properly",
        "Feeling like I'm drowning in problems",
        "Terrible anxiety, can't sleep at night",
        "Breaking down from all the pressure"
    ]
    
    data = []
    
    for _ in range(n_samples):
        category = np.random.choice(['steady', 'drifting', 'overboard'], p=[0.4, 0.4, 0.2])
        
        if category == 'steady':
            text = np.random.choice(steady_texts)
        elif category == 'drifting':
            text = np.random.choice(drifting_texts)
        else:
            text = np.random.choice(overboard_texts)
        
        data.append({
            'text': text,
            'stress_level': category
        })
    
    return pd.DataFrame(data)


# Create singleton instance
analyzer = SentimentAnalyzer()


def analyze_mood_text(text):
    """Convenience function for text analysis"""
    return analyzer.analyze_text(text)


def analyze_mood_questionnaire(responses):
    """Convenience function for questionnaire analysis"""
    return analyzer.analyze_questionnaire(responses)
