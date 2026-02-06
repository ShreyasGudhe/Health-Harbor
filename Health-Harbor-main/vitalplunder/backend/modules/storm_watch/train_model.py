"""
Storm Watch - Health Risk Training Module
==========================================
Module 1: Health Risk Scanner

This module trains a Random Forest classifier to predict health risk levels
based on user health metrics like age, BMI, activity level, etc.

Risk Levels (Pirate Theme):
- Calm Seas (0): Low risk - smooth sailing ahead
- Rising Storm (1): Moderate risk - be cautious
- High Alert (2): High risk - take immediate action

Author: VitalPlunder Team
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os


def generate_sample_dataset(n_samples=1000):
    """
    Generate a synthetic health dataset for training
    
    This creates realistic health data with correlations between
    features and health risk outcomes.
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        DataFrame with health features and risk labels
    """
    np.random.seed(42)  # For reproducibility
    
    # Generate base features
    data = {
        'age': np.random.randint(18, 80, n_samples),
        'gender': np.random.choice(['male', 'female'], n_samples),
        'bmi': np.random.uniform(16, 40, n_samples),
        'activity_level': np.random.choice(['sedentary', 'light', 'moderate', 'active', 'very_active'], n_samples),
        'diet_quality': np.random.choice(['poor', 'fair', 'good', 'excellent'], n_samples),
        'sleep_hours': np.random.uniform(3, 12, n_samples),
        'smoking': np.random.choice([0, 1], n_samples, p=[0.75, 0.25]),
        'alcohol_weekly': np.random.randint(0, 21, n_samples),
        'stress_level': np.random.randint(1, 11, n_samples),
        'family_history': np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
    }
    
    df = pd.DataFrame(data)
    
    # Calculate risk score based on realistic health factors
    # Higher score = higher risk
    risk_score = np.zeros(n_samples)
    
    # Age factor (higher age = higher risk)
    risk_score += (df['age'] - 18) / 62 * 20
    
    # BMI factor (deviation from healthy range 18.5-24.9)
    bmi_deviation = np.abs(df['bmi'] - 22)
    risk_score += bmi_deviation * 1.5
    
    # Activity level factor
    activity_map = {'sedentary': 15, 'light': 10, 'moderate': 5, 'active': 2, 'very_active': 0}
    risk_score += df['activity_level'].map(activity_map)
    
    # Diet quality factor
    diet_map = {'poor': 15, 'fair': 8, 'good': 3, 'excellent': 0}
    risk_score += df['diet_quality'].map(diet_map)
    
    # Sleep factor (optimal is 7-9 hours)
    sleep_deviation = np.abs(df['sleep_hours'] - 8)
    risk_score += sleep_deviation * 3
    
    # Smoking factor
    risk_score += df['smoking'] * 20
    
    # Alcohol factor
    risk_score += df['alcohol_weekly'] * 0.5
    
    # Stress factor
    risk_score += df['stress_level'] * 2
    
    # Family history factor
    risk_score += df['family_history'] * 10
    
    # Add some random noise
    risk_score += np.random.normal(0, 5, n_samples)
    
    # Convert to risk levels
    # Calm Seas: 0-40, Rising Storm: 40-70, High Alert: 70+
    df['risk_level'] = pd.cut(
        risk_score,
        bins=[-np.inf, 40, 70, np.inf],
        labels=['calm_seas', 'rising_storm', 'high_alert']
    )
    
    return df


def preprocess_data(df):
    """
    Preprocess the health data for training
    
    Args:
        df: Raw DataFrame
        
    Returns:
        X: Feature matrix
        y: Target labels
        encoders: Dictionary of fitted encoders
        scaler: Fitted StandardScaler
    """
    encoders = {}
    
    # Encode categorical variables
    categorical_cols = ['gender', 'activity_level', 'diet_quality']
    df_encoded = df.copy()
    
    for col in categorical_cols:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df[col])
        encoders[col] = le
    
    # Encode target variable
    target_encoder = LabelEncoder()
    y = target_encoder.fit_transform(df['risk_level'])
    encoders['risk_level'] = target_encoder
    
    # Select features
    feature_cols = ['age', 'gender', 'bmi', 'activity_level', 'diet_quality', 
                    'sleep_hours', 'smoking', 'alcohol_weekly', 'stress_level', 'family_history']
    X = df_encoded[feature_cols].values
    
    # Scale features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    return X, y, encoders, scaler, feature_cols


def train_model(X, y):
    """
    Train the Random Forest health risk classifier
    
    Args:
        X: Feature matrix
        y: Target labels
        
    Returns:
        Trained model and test metrics
    """
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Initialize Random Forest with parameters that train quickly in local/dev
    # environments (and avoid heavy parallelism issues on some Windows setups).
    model = RandomForestClassifier(
        n_estimators=50,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=1,
    )
    
    # Train the model
    print("⚓ Training Storm Watch model...")
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n📊 Model Accuracy: {accuracy:.2%}")
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Calm Seas', 'Rising Storm', 'High Alert']))
    
    # Feature importance
    print("\n🎯 Feature Importance:")
    feature_names = ['age', 'gender', 'bmi', 'activity_level', 'diet_quality', 
                     'sleep_hours', 'smoking', 'alcohol_weekly', 'stress_level', 'family_history']
    importance = model.feature_importances_
    for name, imp in sorted(zip(feature_names, importance), key=lambda x: x[1], reverse=True):
        print(f"  {name}: {imp:.3f}")
    
    return model, accuracy


def save_model(model, encoders, scaler, feature_cols, save_dir=None):
    """
    Save the trained model and preprocessing objects
    
    Args:
        model: Trained model
        encoders: Dictionary of label encoders
        scaler: Fitted scaler
        feature_cols: List of feature column names
        save_dir: Directory to save files
    """
    if save_dir is None:
        save_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Save model
    model_path = os.path.join(save_dir, 'health_risk_model.pkl')
    joblib.dump(model, model_path)
    print(f"\n✅ Model saved to: {model_path}")
    
    # Save encoders
    encoders_path = os.path.join(save_dir, 'encoders.pkl')
    joblib.dump(encoders, encoders_path)
    print(f"✅ Encoders saved to: {encoders_path}")
    
    # Save scaler
    scaler_path = os.path.join(save_dir, 'scaler.pkl')
    joblib.dump(scaler, scaler_path)
    print(f"✅ Scaler saved to: {scaler_path}")
    
    # Save feature columns
    features_path = os.path.join(save_dir, 'feature_cols.pkl')
    joblib.dump(feature_cols, features_path)
    print(f"✅ Feature columns saved to: {features_path}")


def main():
    """
    Main training pipeline
    """
    print("=" * 50)
    print("⚓ Storm Watch - Health Risk Model Training ⚓")
    print("=" * 50)
    
    # Generate dataset
    print("\n📊 Generating sample dataset...")
    # Keep this modest so first-run setup is fast.
    df = generate_sample_dataset(n_samples=800)
    
    # Save dataset for reference
    dataset_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'datasets')
    os.makedirs(dataset_dir, exist_ok=True)
    dataset_path = os.path.join(dataset_dir, 'health_risk_dataset.csv')
    df.to_csv(dataset_path, index=False)
    print(f"✅ Dataset saved to: {dataset_path}")
    
    # Preprocess
    print("\n🔧 Preprocessing data...")
    X, y, encoders, scaler, feature_cols = preprocess_data(df)
    
    # Train
    model, accuracy = train_model(X, y)
    
    # Save
    save_model(model, encoders, scaler, feature_cols)
    
    print("\n" + "=" * 50)
    print("⚓ Storm Watch training complete! ⚓")
    print("=" * 50)


if __name__ == '__main__':
    main()
