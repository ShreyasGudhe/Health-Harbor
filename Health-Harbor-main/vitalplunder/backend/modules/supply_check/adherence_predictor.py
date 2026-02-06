"""
Supply Check - Adherence Predictor
==================================
Module 4: Medication Adherence Predictor

Extended medication tracking and schedule management.

Author: VitalPlunder Team
"""

from datetime import datetime, timedelta
from .medication_model import medication_model


class AdherencePredictor:
    """
    Medication Schedule Management and Adherence Tracking
    """
    
    def __init__(self):
        """Initialize adherence predictor"""
        self.model = medication_model
    
    def analyze_schedule(self, medications):
        """
        Analyze a medication schedule for adherence risks
        
        Args:
            medications: List of medication dictionaries with:
                - name: Medication name
                - dosage: Dosage string
                - times: List of scheduled times (HH:MM format)
                - frequency: 'daily', 'weekly', 'as_needed'
                
        Returns:
            Schedule analysis with risk assessment for each medication
        """
        analysis = []
        current_hour = datetime.now().hour
        current_day = datetime.now().weekday()
        
        for med in medications:
            med_analysis = {
                'name': med.get('name', 'Unknown'),
                'dosage': med.get('dosage', 'N/A'),
                'frequency': med.get('frequency', 'daily'),
                'times': med.get('times', []),
                'dose_predictions': []
            }
            
            # Analyze each scheduled time
            for time_str in med.get('times', []):
                try:
                    hour = int(time_str.split(':')[0])
                    
                    prediction_data = {
                        'hour_of_day': hour,
                        'day_of_week': current_day,
                        'missed_last_7_days': med.get('missed_last_7_days', 0),
                        'consecutive_taken': med.get('consecutive_taken', 0),
                        'medication_count': len(medications),
                        'reminder_set': med.get('reminder_set', 1)
                    }
                    
                    prediction = self.model.predict_adherence(prediction_data)
                    
                    med_analysis['dose_predictions'].append({
                        'scheduled_time': time_str,
                        'miss_risk': prediction['miss_probability'],
                        'risk_level': prediction['risk_level']
                    })
                    
                except (ValueError, IndexError):
                    continue
            
            # Calculate overall medication risk
            if med_analysis['dose_predictions']:
                avg_risk = sum(d['miss_risk'] for d in med_analysis['dose_predictions']) / len(med_analysis['dose_predictions'])
                med_analysis['overall_risk'] = round(avg_risk, 1)
            else:
                med_analysis['overall_risk'] = 0
            
            analysis.append(med_analysis)
        
        # Sort by risk (highest first)
        analysis.sort(key=lambda x: x['overall_risk'], reverse=True)
        
        return {
            'success': True,
            'medications_analyzed': len(analysis),
            'analysis': analysis,
            'high_risk_count': sum(1 for m in analysis if m['overall_risk'] > 50)
        }
    
    def get_next_doses(self, medications, hours_ahead=24):
        """
        Get upcoming doses within specified hours
        
        Args:
            medications: List of medication dictionaries
            hours_ahead: Hours to look ahead
            
        Returns:
            List of upcoming doses
        """
        now = datetime.now()
        upcoming = []
        
        for med in medications:
            for time_str in med.get('times', []):
                try:
                    hour, minute = map(int, time_str.split(':'))
                    
                    # Create datetime for today
                    dose_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    
                    # If time has passed today, check tomorrow
                    if dose_time < now:
                        dose_time += timedelta(days=1)
                    
                    # Check if within range
                    if dose_time <= now + timedelta(hours=hours_ahead):
                        # Get prediction for this dose
                        prediction = self.model.predict_adherence({
                            'hour_of_day': hour,
                            'day_of_week': dose_time.weekday(),
                            'missed_last_7_days': med.get('missed_last_7_days', 0),
                            'consecutive_taken': med.get('consecutive_taken', 0),
                            'medication_count': len(medications),
                            'reminder_set': med.get('reminder_set', 1)
                        })
                        
                        upcoming.append({
                            'medication': med.get('name', 'Unknown'),
                            'dosage': med.get('dosage', 'N/A'),
                            'scheduled_time': dose_time.strftime('%Y-%m-%d %H:%M'),
                            'hours_until': round((dose_time - now).total_seconds() / 3600, 1),
                            'risk_level': prediction['risk_level']
                        })
                        
                except (ValueError, IndexError):
                    continue
        
        # Sort by time
        upcoming.sort(key=lambda x: x['hours_until'])
        
        return {
            'success': True,
            'upcoming_doses': upcoming,
            'count': len(upcoming),
            'next_dose': upcoming[0] if upcoming else None
        }
    
    def calculate_adherence_score(self, history):
        """
        Calculate adherence score from history
        
        Args:
            history: List of dose records with 'taken' boolean
            
        Returns:
            Adherence score and statistics
        """
        if not history:
            return {
                'success': False,
                'error': 'No history provided'
            }
        
        total = len(history)
        taken = sum(1 for record in history if record.get('taken', False))
        missed = total - taken
        
        score = (taken / total) * 100 if total > 0 else 0
        
        # Determine grade
        if score >= 95:
            grade = {'letter': 'A+', 'label': 'Excellent', 'emoji': '🏆'}
        elif score >= 85:
            grade = {'letter': 'A', 'label': 'Great', 'emoji': '⭐'}
        elif score >= 75:
            grade = {'letter': 'B', 'label': 'Good', 'emoji': '👍'}
        elif score >= 65:
            grade = {'letter': 'C', 'label': 'Fair', 'emoji': '💪'}
        else:
            grade = {'letter': 'D', 'label': 'Needs Improvement', 'emoji': '🚨'}
        
        return {
            'success': True,
            'adherence_score': round(score, 1),
            'total_doses': total,
            'doses_taken': taken,
            'doses_missed': missed,
            'grade': grade
        }


# Create singleton instance
adherence_predictor = AdherencePredictor()


def analyze_medication_schedule(medications):
    """Convenience function for schedule analysis"""
    return adherence_predictor.analyze_schedule(medications)


def get_upcoming_doses(medications, hours_ahead=24):
    """Convenience function for getting upcoming doses"""
    return adherence_predictor.get_next_doses(medications, hours_ahead)


def calculate_adherence_score(history):
    """Convenience function for adherence score calculation"""
    return adherence_predictor.calculate_adherence_score(history)
