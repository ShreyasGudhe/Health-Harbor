"""
Night Watch - Sleep Analyzer
============================
Module 5: Sleep Quality Analyzer

Extended sleep analysis with recommendations and tracking.

Author: VitalPlunder Team
"""

from datetime import datetime, timedelta
from .sleep_model import sleep_model


class SleepAnalyzer:
    """
    Comprehensive Sleep Analysis Engine
    """
    
    # Sleep recommendations based on issues
    RECOMMENDATIONS = {
        'short_sleep': {
            'title': 'Insufficient Sleep Duration',
            'tips': [
                'Aim for 7-9 hours of sleep',
                'Set a consistent bedtime',
                'Avoid sleeping in on weekends',
                'Calculate your ideal wake time backwards from needed hours'
            ],
            'priority': 'high'
        },
        'long_sleep': {
            'title': 'Excessive Sleep',
            'tips': [
                'Too much sleep can indicate underlying issues',
                'Try setting an alarm',
                'Get morning sunlight exposure',
                'Check with a doctor if persistent'
            ],
            'priority': 'medium'
        },
        'late_bedtime': {
            'title': 'Late Bedtime',
            'tips': [
                'Aim to sleep before 11 PM',
                'Start wind-down routine 1 hour before bed',
                'Gradually shift bedtime earlier by 15 minutes',
                'Avoid stimulating activities late at night'
            ],
            'priority': 'high'
        },
        'inconsistent_schedule': {
            'title': 'Inconsistent Sleep Schedule',
            'tips': [
                'Keep same bedtime on weekdays and weekends',
                'Set a consistent wake time',
                'Your body prefers routine',
                'Avoid large schedule variations'
            ],
            'priority': 'medium'
        },
        'screen_before_bed': {
            'title': 'Screen Time Before Bed',
            'tips': [
                'Avoid screens 1-2 hours before bed',
                'Use blue light filters if necessary',
                'Try reading a physical book instead',
                'Keep devices out of bedroom'
            ],
            'priority': 'medium'
        },
        'caffeine_timing': {
            'title': 'Caffeine Too Close to Bedtime',
            'tips': [
                'Avoid caffeine after 2 PM',
                'Caffeine has a 6-hour half-life',
                'Switch to decaf in afternoon',
                'Try herbal tea instead'
            ],
            'priority': 'medium'
        }
    }
    
    def __init__(self):
        """Initialize sleep analyzer"""
        self.model = sleep_model
    
    def analyze_sleep(self, sleep_data):
        """
        Comprehensive sleep analysis
        
        Args:
            sleep_data: Dictionary with sleep parameters
            
        Returns:
            Complete analysis with score, issues, and recommendations
        """
        # Get base prediction
        prediction = self.model.predict_quality(sleep_data)
        
        # Identify issues
        issues = self._identify_issues(sleep_data)
        
        # Get recommendations
        recommendations = self._get_recommendations(issues)
        
        # Generate sleep advice
        advice = self._generate_advice(sleep_data, prediction['quality_score'])
        
        return {
            'success': True,
            'quality_score': prediction['quality_score'],
            'quality_level': prediction['quality_level'],
            'issues_found': len(issues),
            'issues': issues,
            'recommendations': recommendations,
            'advice': advice,
            'sleep_data': prediction['factors']
        }
    
    def _identify_issues(self, sleep_data):
        """Identify sleep issues from data"""
        issues = []
        
        # Check sleep duration
        sleep_hours = sleep_data.get('sleep_hours', 7)
        if sleep_hours < 6:
            issues.append('short_sleep')
        elif sleep_hours > 9:
            issues.append('long_sleep')
        
        # Check bedtime
        bedtime = sleep_data.get('bedtime', '23:00')
        if isinstance(bedtime, str) and ':' in bedtime:
            hour = int(bedtime.split(':')[0])
            if hour >= 24 or hour < 4:  # After midnight
                issues.append('late_bedtime')
            elif hour >= 23:
                issues.append('late_bedtime')
        
        # Check consistency
        consistency = sleep_data.get('consistency_score', 50)
        if consistency < 50:
            issues.append('inconsistent_schedule')
        
        # Check screen time
        screen_hours = sleep_data.get('screen_hours_before', 1)
        if screen_hours > 1:
            issues.append('screen_before_bed')
        
        # Check caffeine
        caffeine_hours = sleep_data.get('caffeine_hours_before', 6)
        if caffeine_hours < 4:
            issues.append('caffeine_timing')
        
        return issues
    
    def _get_recommendations(self, issues):
        """Get recommendations based on identified issues"""
        recommendations = []
        
        for issue in issues:
            if issue in self.RECOMMENDATIONS:
                recommendations.append(self.RECOMMENDATIONS[issue])
        
        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        recommendations.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 99))
        
        return recommendations
    
    def _generate_advice(self, sleep_data, quality_score):
        """Generate personalized sleep advice"""
        if quality_score >= 80:
            return {
                'summary': 'Excellent sleep quality! Keep up the good habits.',
                'focus_area': 'Maintenance',
                'tips': [
                    'Maintain your current sleep routine',
                    'Consider tracking patterns over time',
                    'Share your habits with others'
                ]
            }
        elif quality_score >= 60:
            return {
                'summary': 'Good sleep, with room for improvement.',
                'focus_area': 'Optimization',
                'tips': [
                    'Fine-tune your bedtime routine',
                    'Address any minor issues identified',
                    'Monitor progress over next week'
                ]
            }
        elif quality_score >= 40:
            return {
                'summary': 'Sleep quality needs attention.',
                'focus_area': 'Improvement',
                'tips': [
                    'Focus on the top recommendations',
                    'Start with one change at a time',
                    'Track your sleep for patterns'
                ]
            }
        else:
            return {
                'summary': 'Sleep quality is concerning. Take action.',
                'focus_area': 'Priority',
                'tips': [
                    'Address issues immediately',
                    'Consider consulting a doctor',
                    'Make sleep a top priority'
                ]
            }
    
    def calculate_ideal_bedtime(self, wake_time, target_hours=8):
        """
        Calculate ideal bedtime for desired wake time
        
        Args:
            wake_time: Desired wake time (HH:MM)
            target_hours: Target sleep hours
            
        Returns:
            Ideal bedtime
        """
        try:
            if isinstance(wake_time, str) and ':' in wake_time:
                hour, minute = map(int, wake_time.split(':'))
                wake_datetime = datetime.now().replace(hour=hour, minute=minute)
                
                # Subtract target hours plus 15 min for falling asleep
                bedtime = wake_datetime - timedelta(hours=target_hours, minutes=15)
                
                return {
                    'success': True,
                    'ideal_bedtime': bedtime.strftime('%H:%M'),
                    'target_hours': target_hours,
                    'wake_time': wake_time,
                    'note': 'Includes 15 minutes to fall asleep'
                }
        except:
            pass
        
        return {
            'success': False,
            'error': 'Invalid wake time format'
        }
    
    def get_sleep_cycles(self, bedtime, cycles=5):
        """
        Calculate optimal wake times based on sleep cycles
        
        Args:
            bedtime: Planned bedtime (HH:MM)
            cycles: Number of cycles to calculate
            
        Returns:
            List of optimal wake times
        """
        try:
            if isinstance(bedtime, str) and ':' in bedtime:
                hour, minute = map(int, bedtime.split(':'))
                bed_datetime = datetime.now().replace(hour=hour, minute=minute)
                
                # Add 15 min to fall asleep
                sleep_start = bed_datetime + timedelta(minutes=15)
                
                # Each sleep cycle is ~90 minutes
                wake_times = []
                for i in range(3, cycles + 1):
                    wake_time = sleep_start + timedelta(minutes=90 * i)
                    sleep_hours = (90 * i) / 60
                    wake_times.append({
                        'wake_time': wake_time.strftime('%H:%M'),
                        'sleep_hours': round(sleep_hours, 1),
                        'cycles': i,
                        'recommendation': 'Optimal' if 5 <= i <= 6 else 'Acceptable'
                    })
                
                return {
                    'success': True,
                    'bedtime': bedtime,
                    'wake_options': wake_times
                }
        except:
            pass
        
        return {
            'success': False,
            'error': 'Invalid bedtime format'
        }


# Create singleton instance
sleep_analyzer = SleepAnalyzer()


def analyze_sleep(sleep_data):
    """Convenience function for comprehensive sleep analysis"""
    return sleep_analyzer.analyze_sleep(sleep_data)


def calculate_ideal_bedtime(wake_time, target_hours=8):
    """Calculate ideal bedtime"""
    return sleep_analyzer.calculate_ideal_bedtime(wake_time, target_hours)


def get_sleep_cycles(bedtime, cycles=5):
    """Get optimal wake times based on sleep cycles"""
    return sleep_analyzer.get_sleep_cycles(bedtime, cycles)
