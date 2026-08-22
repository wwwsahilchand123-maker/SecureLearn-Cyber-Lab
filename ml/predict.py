# ml/predict.py
"""
ML Prediction Service
Educational Phishing Detection Simulator
"""

import joblib
import numpy as np
from typing import Dict, Tuple
import os

class PhishingPredictor:
    """Phishing prediction using trained model"""
    
    def __init__(self, model_path='ml/model/phishing_model.pkl'):
        """Initialize predictor"""
        self.model_path = model_path if os.path.isabs(model_path) else os.path.join(os.path.dirname(os.path.dirname(__file__)), model_path)
        self.model = None
        self.feature_names = []
        self.load_model()
    
    def load_model(self):
        """Load trained model"""
        if not os.path.exists(self.model_path):
            print(f"[WARNING] Model not found at {self.model_path}")
            print("Please run: python ml/train_model.py")
            return False
        
        try:
            model_data = joblib.load(self.model_path)
            self.model = model_data['model']
            self.feature_names = model_data['feature_names']
            print(f"[OK] Model loaded from: {self.model_path}")
            return True
        except Exception as e:
            print(f"[ERROR] Error loading model: {e}")
            return False
    
    def predict(self, features: Dict) -> Tuple[str, float, Dict]:
        """
        Predict if URL/email is phishing
        
        Returns:
            prediction: 'phishing' or 'legitimate'
            confidence: probability score
            explanation: feature contributions
        """
        if self.model is None:
            return 'unknown', 0.0, {}
        
        # Ensure all features are present
        feature_vector = []
        for feature_name in self.feature_names:
            feature_vector.append(features.get(feature_name, 0))
        
        # Predict
        prediction_proba = self.model.predict_proba([feature_vector])[0]
        prediction = 'legitimate' if prediction_proba[0] > prediction_proba[1] else 'phishing'
        confidence = max(prediction_proba)
        
        # Get feature importance for explanation
        feature_importance = self.model.feature_importances_
        feature_contributions = {}
        
        for i, feature_name in enumerate(self.feature_names):
            if features.get(feature_name, 0) > 0:
                feature_contributions[feature_name] = {
                    'value': features.get(feature_name, 0),
                    'importance': float(feature_importance[i])
                }
        
        # Sort by importance
        sorted_contributions = dict(
            sorted(feature_contributions.items(), 
                  key=lambda x: x[1]['importance'], 
                  reverse=True)
        )
        
        return prediction, float(confidence), sorted_contributions

# Test the predictor
if __name__ == '__main__':
    predictor = PhishingPredictor()
    
    # Test phishing features
    phishing_features = {
        'url_length': 150,
        'num_dots': 7,
        'num_hyphens': 5,
        'num_underscores': 3,
        'num_slashes': 6,
        'num_digits': 15,
        'num_params': 8,
        'has_ip': 1,
        'has_https': 0,
        'suspicious_tld': 1,
        'domain_length': 35,
        'num_subdomains': 4,
        'has_at_symbol': 1,
        'has_double_slash': 1,
        'entropy': 4.5,
    }
    
    prediction, confidence, explanation = predictor.predict(phishing_features)
    print(f"\nPrediction: {prediction}")
    print(f"Confidence: {confidence:.2%}")
    print("\nTop Contributing Features:")
    for feature, data in list(explanation.items())[:5]:
        print(f"  {feature}: {data['value']} (importance: {data['importance']:.4f})")