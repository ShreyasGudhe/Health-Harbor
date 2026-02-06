"""
Mind Compass - Stress Predictor
===============================
Module 2: Mental Health & Stress Monitor

Extended stress prediction with recommendations and tracking.

Author: VitalPlunder Team
"""

from .sentiment_model import analyzer


class StressPredictor:
    """
    Advanced Stress Prediction and Recommendation Engine
    """
    
    # Recommendations based on stress level
    RECOMMENDATIONS = {
        'steady': [
            {
                'title': 'Maintain Your Course',
                'description': 'Keep up with your current healthy habits',
                'icon': '⚓'
            },
            {
                'title': 'Practice Gratitude',
                'description': 'Continue journaling positive experiences',
                'icon': '📝'
            },
            {
                'title': 'Stay Connected',
                'description': 'Maintain your social connections',
                'icon': '🤝'
            }
        ],
        'drifting': [
            {
                'title': 'Take a Break',
                'description': 'Step away from stressors for 10-15 minutes',
                'icon': '☕'
            },
            {
                'title': 'Deep Breathing',
                'description': 'Try 4-7-8 breathing technique',
                'icon': '🧘'
            },
            {
                'title': 'Go for a Walk',
                'description': '15 minutes of fresh air can help reset',
                'icon': '🚶'
            },
            {
                'title': 'Talk to Someone',
                'description': 'Share your feelings with a trusted friend',
                'icon': '💬'
            },
            {
                'title': 'Prioritize Sleep',
                'description': 'Aim for 7-9 hours tonight',
                'icon': '😴'
            }
        ],
        'overboard': [
            {
                'title': 'Seek Support',
                'description': 'Consider talking to a mental health professional',
                'icon': '🏥'
            },
            {
                'title': 'Emergency Grounding',
                'description': 'Use 5-4-3-2-1 grounding technique',
                'icon': '🌍'
            },
            {
                'title': 'Reach Out Now',
                'description': 'Call a friend or family member right away',
                'icon': '📞'
            },
            {
                'title': 'Self-Compassion',
                'description': "It's okay to not be okay. Be gentle with yourself",
                'icon': '❤️'
            },
            {
                'title': 'Crisis Resources',
                'description': 'If in crisis, please contact a helpline',
                'icon': '🆘'
            }
        ]
    }
    
    # Coping techniques
    COPING_TECHNIQUES = {
        'breathing': {
            'name': '4-7-8 Breathing',
            'steps': [
                'Breathe in quietly through your nose for 4 seconds',
                'Hold your breath for 7 seconds',
                'Exhale completely through your mouth for 8 seconds',
                'Repeat 3-4 times'
            ]
        },
        'grounding': {
            'name': '5-4-3-2-1 Grounding',
            'steps': [
                'Name 5 things you can SEE',
                'Name 4 things you can TOUCH',
                'Name 3 things you can HEAR',
                'Name 2 things you can SMELL',
                'Name 1 thing you can TASTE'
            ]
        },
        'progressive_relaxation': {
            'name': 'Progressive Muscle Relaxation',
            'steps': [
                'Tense your feet muscles for 5 seconds, then release',
                'Move to calves, thighs, abdomen, chest',
                'Continue with hands, arms, shoulders, neck, face',
                'Focus on the contrast between tension and relaxation'
            ]
        }
    }
    
    def predict_stress(self, input_data, input_type='text'):
        """
        Main prediction method that handles both text and questionnaire input
        
        Args:
            input_data: Either text string or questionnaire dict
            input_type: 'text' or 'questionnaire'
            
        Returns:
            Complete stress assessment with recommendations
        """
        # Get base analysis
        if input_type == 'text':
            analysis = analyzer.analyze_text(input_data)
        else:
            analysis = analyzer.analyze_questionnaire(input_data)
        
        if not analysis.get('success'):
            return analysis
        
        # Get stress level code
        stress_code = analysis['stress_level']['code']
        stress_score = analysis['stress_score']
        
        # Add recommendations
        analysis['recommendations'] = self.RECOMMENDATIONS.get(stress_code, [])
        
        # Add appropriate coping technique
        if stress_code == 'overboard':
            analysis['immediate_technique'] = self.COPING_TECHNIQUES['grounding']
        elif stress_code == 'drifting':
            analysis['immediate_technique'] = self.COPING_TECHNIQUES['breathing']
        else:
            analysis['immediate_technique'] = None
        
        # Add trend indicator (placeholder - would need historical data)
        analysis['trend'] = self._get_trend_placeholder()
        
        # Add wellness tips
        analysis['daily_tips'] = self._get_daily_tips(stress_code)
        
        return analysis
    
    def _get_trend_placeholder(self):
        """
        Placeholder for trend analysis
        TODO: Implement with actual historical tracking
        """
        return {
            'direction': 'stable',
            'message': 'Track regularly to see your mental health trends',
            'data_points': 0
        }
    
    def _get_daily_tips(self, stress_code):
        """
        Get daily wellness tips based on stress level
        
        Args:
            stress_code: Current stress level code
            
        Returns:
            List of daily tips
        """
        general_tips = [
            'Stay hydrated - drink at least 8 glasses of water',
            'Take short breaks every hour when working',
            'Practice mindfulness for 5 minutes daily',
            'Limit screen time before bed',
            'Connect with nature when possible'
        ]
        
        if stress_code == 'overboard':
            return [
                'Focus on basic needs: eat, sleep, hydrate',
                'It\'s okay to say no to additional commitments',
                'Consider reaching out to a professional',
                'Take things one small step at a time'
            ]
        elif stress_code == 'drifting':
            return [
                'Identify your top 3 stressors',
                'Schedule dedicated relaxation time',
                'Try a new stress-relief activity',
                'Review your sleep schedule'
            ]
        else:
            return general_tips[:3]
    
    def get_mood_history_template(self):
        """
        Get template for mood tracking history
        
        Returns:
            Template structure for frontend mood tracking
        """
        return {
            'daily_check_in': {
                'mood_rating': {'min': 1, 'max': 10, 'label': 'How are you feeling?'},
                'energy_level': {'min': 1, 'max': 10, 'label': 'Energy level?'},
                'anxiety_level': {'min': 1, 'max': 10, 'label': 'Anxiety level?'},
                'sleep_quality': {'min': 1, 'max': 10, 'label': 'How was your sleep?'},
                'notes': {'type': 'text', 'label': 'Any thoughts to share?'}
            },
            'quick_check': {
                'mood': {'options': ['😊', '🙂', '😐', '😔', '😰'], 'label': 'Quick mood check'}
            }
        }


# Create singleton instance
stress_predictor = StressPredictor()


def predict_stress_level(input_data, input_type='text'):
    """Convenience function for stress prediction"""
    return stress_predictor.predict_stress(input_data, input_type)


def get_coping_technique(technique_name):
    """Get a specific coping technique"""
    return stress_predictor.COPING_TECHNIQUES.get(technique_name)


def get_all_coping_techniques():
    """Get all available coping techniques"""
    return stress_predictor.COPING_TECHNIQUES
