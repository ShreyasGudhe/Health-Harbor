"""
Galley Log - Nutrition Mapper
=============================
Module 6: Diet & Nutrition Tracker

Maps food items to nutritional information.

Author: VitalPlunder Team
"""

import os
import json


class NutritionMapper:
    """
    Nutrition Database and Mapper
    
    Maps food items to nutritional values (calories, protein, carbs, fats).
    """
    
    # Nutrition database (per 100g unless otherwise noted)
    NUTRITION_DB = {
        # Proteins
        'chicken_breast': {
            'name': 'Chicken Breast (grilled)',
            'calories': 165,
            'protein': 31,
            'carbs': 0,
            'fat': 3.6,
            'fiber': 0,
            'serving': '100g'
        },
        'chicken': {
            'name': 'Chicken',
            'calories': 239,
            'protein': 27,
            'carbs': 0,
            'fat': 14,
            'fiber': 0,
            'serving': '100g'
        },
        'salmon': {
            'name': 'Salmon',
            'calories': 208,
            'protein': 20,
            'carbs': 0,
            'fat': 13,
            'fiber': 0,
            'serving': '100g'
        },
        'fish': {
            'name': 'Fish (average)',
            'calories': 140,
            'protein': 22,
            'carbs': 0,
            'fat': 5,
            'fiber': 0,
            'serving': '100g'
        },
        'eggs': {
            'name': 'Eggs',
            'calories': 155,
            'protein': 13,
            'carbs': 1.1,
            'fat': 11,
            'fiber': 0,
            'serving': '2 eggs (100g)'
        },
        
        # Grains & Carbs
        'rice': {
            'name': 'White Rice (cooked)',
            'calories': 130,
            'protein': 2.7,
            'carbs': 28,
            'fat': 0.3,
            'fiber': 0.4,
            'serving': '100g'
        },
        'rice_dish': {
            'name': 'Rice Dish',
            'calories': 180,
            'protein': 5,
            'carbs': 32,
            'fat': 4,
            'fiber': 1,
            'serving': '200g'
        },
        'pasta': {
            'name': 'Pasta (cooked)',
            'calories': 131,
            'protein': 5,
            'carbs': 25,
            'fat': 1.1,
            'fiber': 1.8,
            'serving': '100g'
        },
        'bread': {
            'name': 'Bread',
            'calories': 265,
            'protein': 9,
            'carbs': 49,
            'fat': 3.2,
            'fiber': 2.7,
            'serving': '1 slice (30g)'
        },
        
        # Main Dishes
        'pizza': {
            'name': 'Pizza (cheese)',
            'calories': 266,
            'protein': 11,
            'carbs': 33,
            'fat': 10,
            'fiber': 2.3,
            'serving': '1 slice (100g)'
        },
        'sandwich': {
            'name': 'Sandwich',
            'calories': 250,
            'protein': 12,
            'carbs': 30,
            'fat': 9,
            'fiber': 2,
            'serving': '1 sandwich (150g)'
        },
        'burger': {
            'name': 'Burger',
            'calories': 295,
            'protein': 17,
            'carbs': 24,
            'fat': 14,
            'fiber': 1,
            'serving': '1 burger (150g)'
        },
        'soup': {
            'name': 'Soup',
            'calories': 60,
            'protein': 3,
            'carbs': 8,
            'fat': 2,
            'fiber': 1,
            'serving': '250ml'
        },
        
        # Vegetables & Salads
        'salad': {
            'name': 'Mixed Salad',
            'calories': 20,
            'protein': 1.5,
            'carbs': 3,
            'fat': 0.2,
            'fiber': 2,
            'serving': '100g'
        },
        'salad_with_dressing': {
            'name': 'Salad with Dressing',
            'calories': 120,
            'protein': 3,
            'carbs': 8,
            'fat': 8,
            'fiber': 3,
            'serving': '200g'
        },
        
        # Fruits
        'fruit': {
            'name': 'Mixed Fruit',
            'calories': 50,
            'protein': 0.5,
            'carbs': 12,
            'fat': 0.2,
            'fiber': 2,
            'serving': '100g'
        },
        'apple': {
            'name': 'Apple',
            'calories': 52,
            'protein': 0.3,
            'carbs': 14,
            'fat': 0.2,
            'fiber': 2.4,
            'serving': '1 medium (180g)'
        },
        'banana': {
            'name': 'Banana',
            'calories': 89,
            'protein': 1.1,
            'carbs': 23,
            'fat': 0.3,
            'fiber': 2.6,
            'serving': '1 medium (120g)'
        },
        
        # Desserts
        'dessert': {
            'name': 'Dessert',
            'calories': 350,
            'protein': 4,
            'carbs': 50,
            'fat': 15,
            'fiber': 1,
            'serving': '100g'
        },
        'cake': {
            'name': 'Cake',
            'calories': 350,
            'protein': 4,
            'carbs': 50,
            'fat': 15,
            'fiber': 1,
            'serving': '1 slice (80g)'
        },
        'ice_cream': {
            'name': 'Ice Cream',
            'calories': 207,
            'protein': 3.5,
            'carbs': 24,
            'fat': 11,
            'fiber': 0,
            'serving': '1 scoop (70g)'
        },
        
        # Beverages
        'beverage': {
            'name': 'Beverage',
            'calories': 30,
            'protein': 0,
            'carbs': 8,
            'fat': 0,
            'fiber': 0,
            'serving': '250ml'
        },
        'coffee': {
            'name': 'Coffee (black)',
            'calories': 2,
            'protein': 0.3,
            'carbs': 0,
            'fat': 0,
            'fiber': 0,
            'serving': '250ml'
        },
        'coffee_latte': {
            'name': 'Latte',
            'calories': 120,
            'protein': 6,
            'carbs': 10,
            'fat': 6,
            'fiber': 0,
            'serving': '350ml'
        },
        
        # Snacks
        'snack': {
            'name': 'Snack',
            'calories': 150,
            'protein': 3,
            'carbs': 18,
            'fat': 8,
            'fiber': 1,
            'serving': '50g'
        },
        'chips': {
            'name': 'Chips',
            'calories': 536,
            'protein': 7,
            'carbs': 53,
            'fat': 35,
            'fiber': 4,
            'serving': '30g bag'
        },
        'nuts': {
            'name': 'Mixed Nuts',
            'calories': 607,
            'protein': 20,
            'carbs': 21,
            'fat': 54,
            'fiber': 7,
            'serving': '30g handful'
        },
        
        # Breakfast
        'breakfast': {
            'name': 'Breakfast',
            'calories': 300,
            'protein': 12,
            'carbs': 35,
            'fat': 12,
            'fiber': 3,
            'serving': '1 plate'
        },
        'oatmeal': {
            'name': 'Oatmeal',
            'calories': 68,
            'protein': 2.5,
            'carbs': 12,
            'fat': 1.4,
            'fiber': 1.7,
            'serving': '100g cooked'
        },
        
        # Default/Unknown
        'unknown': {
            'name': 'Food Item',
            'calories': 200,
            'protein': 8,
            'carbs': 25,
            'fat': 8,
            'fiber': 2,
            'serving': '100g'
        }
    }
    
    # Daily recommended values
    DAILY_VALUES = {
        'calories': 2000,
        'protein': 50,
        'carbs': 275,
        'fat': 78,
        'fiber': 28
    }
    
    def __init__(self):
        """Initialize nutrition mapper"""
        pass
    
    def get_nutrition(self, food_category, portion_multiplier=1.0, custom_name=None):
        """
        Get nutrition information for a food category
        
        Args:
            food_category: Category from classifier
            portion_multiplier: Multiply base values (e.g., 1.5 for large portion)
            custom_name: Custom display name
            
        Returns:
            Nutrition information dictionary
        """
        # Get base nutrition data
        nutrition = self.NUTRITION_DB.get(food_category, self.NUTRITION_DB['unknown']).copy()
        
        # Apply portion multiplier
        for key in ['calories', 'protein', 'carbs', 'fat', 'fiber']:
            nutrition[key] = round(nutrition[key] * portion_multiplier, 1)
        
        # Override name if custom provided
        if custom_name:
            nutrition['name'] = custom_name
        
        # Add percentage of daily values
        nutrition['daily_percent'] = {
            'calories': round((nutrition['calories'] / self.DAILY_VALUES['calories']) * 100, 1),
            'protein': round((nutrition['protein'] / self.DAILY_VALUES['protein']) * 100, 1),
            'carbs': round((nutrition['carbs'] / self.DAILY_VALUES['carbs']) * 100, 1),
            'fat': round((nutrition['fat'] / self.DAILY_VALUES['fat']) * 100, 1),
            'fiber': round((nutrition['fiber'] / self.DAILY_VALUES['fiber']) * 100, 1)
        }
        
        return nutrition
    
    def log_meal(self, food_items):
        """
        Log multiple food items as a meal
        
        Args:
            food_items: List of food dictionaries with category and portion
            
        Returns:
            Meal summary with total nutrition
        """
        meal_items = []
        totals = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0,
            'fiber': 0
        }
        
        for item in food_items:
            category = item.get('category', 'unknown')
            portion = item.get('portion_multiplier', 1.0)
            name = item.get('name')
            
            nutrition = self.get_nutrition(category, portion, name)
            meal_items.append(nutrition)
            
            for key in totals:
                totals[key] += nutrition[key]
        
        # Round totals
        totals = {k: round(v, 1) for k, v in totals.items()}
        
        # Calculate daily percentages for totals
        daily_percent = {
            key: round((totals[key] / self.DAILY_VALUES[key]) * 100, 1)
            for key in totals
        }
        
        return {
            'success': True,
            'items': meal_items,
            'item_count': len(meal_items),
            'totals': totals,
            'daily_percent': daily_percent,
            'meal_rating': self._rate_meal(totals)
        }
    
    def _rate_meal(self, totals):
        """Rate the nutritional balance of a meal"""
        calories = totals['calories']
        
        # Ideal meal is 400-700 calories
        if 400 <= calories <= 700:
            cal_rating = 'ideal'
        elif 300 <= calories <= 800:
            cal_rating = 'acceptable'
        elif calories < 300:
            cal_rating = 'light'
        else:
            cal_rating = 'heavy'
        
        # Check protein ratio
        protein_cal_percent = (totals['protein'] * 4 / max(calories, 1)) * 100
        
        if protein_cal_percent >= 20:
            protein_rating = 'high'
        elif protein_cal_percent >= 10:
            protein_rating = 'moderate'
        else:
            protein_rating = 'low'
        
        return {
            'calorie_assessment': cal_rating,
            'protein_assessment': protein_rating,
            'emoji': '🏆' if cal_rating == 'ideal' else '👍' if cal_rating == 'acceptable' else '⚠️'
        }
    
    def get_daily_summary(self, meals):
        """
        Calculate daily nutrition summary from all meals
        
        Args:
            meals: List of meal summaries
            
        Returns:
            Daily nutrition summary
        """
        daily_totals = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0,
            'fiber': 0
        }
        
        for meal in meals:
            if 'totals' in meal:
                for key in daily_totals:
                    daily_totals[key] += meal['totals'].get(key, 0)
        
        daily_totals = {k: round(v, 1) for k, v in daily_totals.items()}
        
        # Calculate remaining
        remaining = {
            key: max(0, round(self.DAILY_VALUES[key] - daily_totals[key], 1))
            for key in daily_totals
        }
        
        # Percentage consumed
        percent_consumed = {
            key: min(100, round((daily_totals[key] / self.DAILY_VALUES[key]) * 100, 1))
            for key in daily_totals
        }
        
        return {
            'success': True,
            'consumed': daily_totals,
            'remaining': remaining,
            'percent_consumed': percent_consumed,
            'recommended': self.DAILY_VALUES.copy(),
            'assessment': self._assess_daily(percent_consumed)
        }
    
    def _assess_daily(self, percent_consumed):
        """Assess daily nutrition status"""
        cal_percent = percent_consumed['calories']
        
        if cal_percent < 50:
            return {
                'status': 'under',
                'message': 'You still have room for more nutrition today.',
                'emoji': '🍽️'
            }
        elif cal_percent <= 100:
            return {
                'status': 'on_track',
                'message': 'You\'re on track for your daily goals!',
                'emoji': '✅'
            }
        elif cal_percent <= 120:
            return {
                'status': 'slight_over',
                'message': 'Slightly over daily target. Consider a light next meal.',
                'emoji': '⚠️'
            }
        else:
            return {
                'status': 'over',
                'message': 'Over daily calorie target. Balance tomorrow.',
                'emoji': '🚨'
            }


# Create singleton instance
nutrition_mapper = NutritionMapper()


def get_food_nutrition(food_category, portion_multiplier=1.0, name=None):
    """Convenience function for getting nutrition"""
    return nutrition_mapper.get_nutrition(food_category, portion_multiplier, name)


def log_meal(food_items):
    """Convenience function for logging a meal"""
    return nutrition_mapper.log_meal(food_items)


def get_daily_summary(meals):
    """Convenience function for daily summary"""
    return nutrition_mapper.get_daily_summary(meals)
