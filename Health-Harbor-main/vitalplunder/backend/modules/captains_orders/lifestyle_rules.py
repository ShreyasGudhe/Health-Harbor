"""
Captain's Orders - Lifestyle Rules Engine
=========================================
Module 3: Lifestyle Coaching Engine

Rule-based recommendation system for lifestyle coaching.

Author: VitalPlunder Team
"""


class LifestyleRules:
    """
    Rule-based Lifestyle Coaching Engine
    
    Provides personalized recommendations based on habit analysis.
    """
    
    # Daily guidance templates
    DAILY_ORDERS = {
        'morning': [
            {
                'title': 'Rise and Shine, Sailor!',
                'orders': [
                    'Drink a glass of water to hydrate',
                    'Stretch for 5 minutes',
                    'Get some natural light exposure',
                    'Plan your day\'s activities'
                ]
            }
        ],
        'afternoon': [
            {
                'title': 'Midday Check-In',
                'orders': [
                    'Take a 10-minute walk break',
                    'Drink water - stay hydrated',
                    'Stand and stretch if sitting',
                    'Have a healthy snack'
                ]
            }
        ],
        'evening': [
            {
                'title': 'Wind Down Protocol',
                'orders': [
                    'Reduce screen brightness',
                    'Light physical activity',
                    'Prepare for quality sleep',
                    'Reflect on the day\'s achievements'
                ]
            }
        ]
    }
    
    def __init__(self):
        """Initialize the rules engine"""
        self.rules = self._define_rules()
    
    def _define_rules(self):
        """
        Define coaching rules based on habit patterns
        
        Returns:
            Dictionary of rules with conditions and recommendations
        """
        return {
            'low_exercise': {
                'condition': lambda h: h.get('exercise_mins', 0) < 20,
                'priority': 'high',
                'recommendation': {
                    'title': 'Get Moving!',
                    'description': 'Your exercise is below recommended levels',
                    'actions': [
                        'Start with a 10-minute walk',
                        'Try desk exercises every hour',
                        'Set a daily step goal',
                        'Find an activity you enjoy'
                    ],
                    'icon': '🏃'
                }
            },
            'excessive_screen': {
                'condition': lambda h: h.get('screen_hours', 0) > 8,
                'priority': 'high',
                'recommendation': {
                    'title': 'Screen Break Needed',
                    'description': 'Too much screen time detected',
                    'actions': [
                        'Follow 20-20-20 rule (every 20 mins, look 20ft away for 20 secs)',
                        'Set screen time limits',
                        'Take regular breaks',
                        'Try blue light filtering'
                    ],
                    'icon': '📱'
                }
            },
            'poor_sleep': {
                'condition': lambda h: h.get('sleep_hours', 7) < 6 or h.get('sleep_hours', 7) > 10,
                'priority': 'high',
                'recommendation': {
                    'title': 'Sleep Schedule Alert',
                    'description': 'Your sleep hours are outside optimal range (7-9 hours)',
                    'actions': [
                        'Set a consistent bedtime',
                        'Avoid screens 1 hour before bed',
                        'Keep bedroom cool and dark',
                        'Limit caffeine after 2 PM'
                    ],
                    'icon': '😴'
                }
            },
            'low_steps': {
                'condition': lambda h: h.get('steps', 0) < 5000,
                'priority': 'medium',
                'recommendation': {
                    'title': 'Step It Up!',
                    'description': 'Daily steps below target',
                    'actions': [
                        'Take stairs instead of elevator',
                        'Walk during phone calls',
                        'Park farther away',
                        'Set hourly movement reminders'
                    ],
                    'icon': '👟'
                }
            },
            'dehydration': {
                'condition': lambda h: h.get('water_glasses', 0) < 6,
                'priority': 'medium',
                'recommendation': {
                    'title': 'Hydration Alert',
                    'description': 'Drink more water today',
                    'actions': [
                        'Keep a water bottle handy',
                        'Set hourly water reminders',
                        'Drink a glass before each meal',
                        'Track your water intake'
                    ],
                    'icon': '💧'
                }
            },
            'balanced_lifestyle': {
                'condition': lambda h: (
                    h.get('exercise_mins', 0) >= 30 and
                    h.get('screen_hours', 10) <= 6 and
                    6.5 <= h.get('sleep_hours', 7) <= 9 and
                    h.get('steps', 0) >= 7000 and
                    h.get('water_glasses', 0) >= 7
                ),
                'priority': 'positive',
                'recommendation': {
                    'title': 'Excellent Work, Captain!',
                    'description': 'Your lifestyle habits are well-balanced',
                    'actions': [
                        'Keep up the great work!',
                        'Consider helping others on their health journey',
                        'Try new healthy activities',
                        'Maintain consistency'
                    ],
                    'icon': '🏆'
                }
            }
        }
    
    def evaluate_habits(self, habits):
        """
        Evaluate habits against all rules
        
        Args:
            habits: Dictionary with daily habits
            
        Returns:
            List of triggered recommendations
        """
        triggered = []
        
        for rule_name, rule in self.rules.items():
            if rule['condition'](habits):
                triggered.append({
                    'rule': rule_name,
                    'priority': rule['priority'],
                    'recommendation': rule['recommendation']
                })
        
        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'positive': 2}
        triggered.sort(key=lambda x: priority_order.get(x['priority'], 99))
        
        return triggered
    
    def get_daily_orders(self, time_of_day='morning', habits=None):
        """
        Get daily orders/guidance
        
        Args:
            time_of_day: 'morning', 'afternoon', or 'evening'
            habits: Optional current habits for personalization
            
        Returns:
            Daily orders object
        """
        orders = self.DAILY_ORDERS.get(time_of_day, self.DAILY_ORDERS['morning'])[0]
        
        # Personalize if habits provided
        if habits:
            personalized_orders = orders.copy()
            personalized_orders['personalized'] = True
            
            # Add specific reminders based on habits
            extras = []
            if habits.get('water_glasses', 0) < 4:
                extras.append('🚨 Priority: Drink more water!')
            if habits.get('exercise_mins', 0) == 0:
                extras.append('🚨 Priority: Get some exercise today!')
            
            if extras:
                personalized_orders['priority_alerts'] = extras
            
            return personalized_orders
        
        return orders
    
    def get_weekly_summary_template(self):
        """
        Get template for weekly lifestyle summary
        
        Returns:
            Weekly summary structure
        """
        return {
            'metrics_to_track': [
                {'key': 'avg_exercise', 'label': 'Average Daily Exercise', 'unit': 'mins'},
                {'key': 'avg_sleep', 'label': 'Average Sleep', 'unit': 'hours'},
                {'key': 'avg_steps', 'label': 'Average Steps', 'unit': 'steps'},
                {'key': 'avg_screen', 'label': 'Average Screen Time', 'unit': 'hours'},
                {'key': 'total_water', 'label': 'Total Water', 'unit': 'glasses'}
            ],
            'achievements': [
                {'condition': 'exercise_streak', 'badge': '🏃 Active Streak'},
                {'condition': 'hydration_goal', 'badge': '💧 Hydration Hero'},
                {'condition': 'sleep_consistency', 'badge': '😴 Sleep Champion'},
                {'condition': 'step_goal', 'badge': '👟 Step Master'}
            ]
        }
    
    def generate_coaching_message(self, score, profile_name):
        """
        Generate personalized coaching message
        
        Args:
            score: Lifestyle score (0-100)
            profile_name: Lifestyle profile name
            
        Returns:
            Coaching message string
        """
        if score >= 80:
            return f"Outstanding work, {profile_name}! You're sailing with the wind. Keep these habits strong!"
        elif score >= 60:
            return f"Good progress, {profile_name}. A few adjustments and you'll be cruising smoothly!"
        elif score >= 40:
            return f"Time to chart a new course, {profile_name}. Focus on the recommendations below."
        else:
            return f"All hands on deck, {profile_name}! Let's work together to improve your health voyage."


# Create singleton instance
lifestyle_rules = LifestyleRules()


def get_recommendations(habits):
    """Get personalized recommendations based on habits"""
    return lifestyle_rules.evaluate_habits(habits)


def get_daily_guidance(time_of_day='morning', habits=None):
    """Get daily guidance/orders"""
    return lifestyle_rules.get_daily_orders(time_of_day, habits)
