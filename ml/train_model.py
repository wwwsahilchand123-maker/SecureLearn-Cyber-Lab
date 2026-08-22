# ml/train_model.py
"""
Machine Learning Model Training
Educational Phishing Detection Simulator
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import os
import json

class PhishingModelTrainer:
    """Train and evaluate phishing detection model"""
    
    def __init__(self):
        self.model = None
        self.feature_names = []
        self.metrics = {}
    
    def create_sample_dataset(self, n_samples=1000):
        """Create a sample dataset for training"""
        np.random.seed(42)
        
        # Generate features
        data = []
        labels = []
        
        for _ in range(n_samples):
            # 50% phishing, 50% legitimate
            is_phishing = np.random.choice([0, 1])
            
            if is_phishing:
                # Phishing URL characteristics
                feature = {
                    'url_length': np.random.randint(50, 200),
                    'num_dots': np.random.randint(3, 10),
                    'num_hyphens': np.random.randint(2, 8),
                    'num_underscores': np.random.randint(1, 5),
                    'num_slashes': np.random.randint(3, 10),
                    'num_digits': np.random.randint(5, 20),
                    'num_params': np.random.randint(2, 10),
                    'has_ip': np.random.choice([0, 1], p=[0.3, 0.7]),
                    'has_https': np.random.choice([0, 1], p=[0.6, 0.4]),
                    'suspicious_tld': np.random.choice([0, 1], p=[0.4, 0.6]),
                    'domain_length': np.random.randint(15, 40),
                    'num_subdomains': np.random.randint(2, 6),
                    'has_at_symbol': np.random.choice([0, 1], p=[0.7, 0.3]),
                    'has_double_slash': np.random.choice([0, 1], p=[0.6, 0.4]),
                    'entropy': np.random.uniform(3.5, 5.0),
                }
            else:
                # Legitimate URL characteristics
                feature = {
                    'url_length': np.random.randint(10, 60),
                    'num_dots': np.random.randint(1, 3),
                    'num_hyphens': np.random.randint(0, 2),
                    'num_underscores': np.random.randint(0, 1),
                    'num_slashes': np.random.randint(1, 4),
                    'num_digits': np.random.randint(0, 5),
                    'num_params': np.random.randint(0, 3),
                    'has_ip': 0,
                    'has_https': np.random.choice([0, 1], p=[0.2, 0.8]),
                    'suspicious_tld': np.random.choice([0, 1], p=[0.9, 0.1]),
                    'domain_length': np.random.randint(5, 20),
                    'num_subdomains': np.random.randint(0, 2),
                    'has_at_symbol': 0,
                    'has_double_slash': 0,
                    'entropy': np.random.uniform(2.0, 3.5),
                }
            
            data.append(feature)
            labels.append(is_phishing)
        
        df = pd.DataFrame(data)
        df['label'] = labels
        
        return df
    
    def train(self, df):
        """Train the model"""
        # Separate features and labels
        X = df.drop('label', axis=1)
        y = df['label']
        
        self.feature_names = X.columns.tolist()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train Random Forest
        print("Training Random Forest Classifier...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        
        self.metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        print("\n" + "="*50)
        print("MODEL EVALUATION RESULTS")
        print("="*50)
        print(f"Accuracy:  {self.metrics['accuracy']:.4f}")
        print(f"Precision: {self.metrics['precision']:.4f}")
        print(f"Recall:    {self.metrics['recall']:.4f}")
        print(f"F1 Score:  {self.metrics['f1_score']:.4f}")
        print("\nConfusion Matrix:")
        print(f"  {self.metrics['confusion_matrix']}")
        print("="*50 + "\n")
        
        return self.metrics
    
    def save_model(self, model_path='ml/model/phishing_model.pkl', 
                   metrics_path='ml/model/metrics.json'):
        """Save trained model and metrics"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Save model
        model_data = {
            'model': self.model,
            'feature_names': self.feature_names
        }
        joblib.dump(model_data, model_path)
        print(f"[OK] Model saved to: {model_path}")
        
        # Save metrics
        with open(metrics_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        print(f"[OK] Metrics saved to: {metrics_path}")
    
    def get_feature_importance(self):
        """Get feature importance"""
        if self.model is None:
            return None
        
        importance = self.model.feature_importances_
        feature_importance = dict(zip(self.feature_names, importance))
        return dict(sorted(feature_importance.items(), 
                          key=lambda x: x[1], reverse=True))

def main():
    """Main training function"""
    print("[*] Starting Phishing Detection Model Training...")
    print("="*50)
    
    trainer = PhishingModelTrainer()
    
    # Create dataset
    print("\n[*] Creating sample dataset...")
    df = trainer.create_sample_dataset(n_samples=2000)
    print(f"Dataset created: {len(df)} samples")
    print(f"Phishing samples: {df['label'].sum()}")
    print(f"Legitimate samples: {len(df) - df['label'].sum()}")
    
    # Save dataset
    dataset_path = 'ml/dataset/phishing_data.csv'
    os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
    df.to_csv(dataset_path, index=False)
    print(f"[OK] Dataset saved to: {dataset_path}")
    
    # Train model
    print("\n[*] Training model...")
    metrics = trainer.train(df)
    
    # Feature importance
    print("\n[*] Feature Importance:")
    feature_importance = trainer.get_feature_importance()
    for feature, importance in list(feature_importance.items())[:10]:
        print(f"  {feature:20s}: {importance:.4f}")
    
    # Save model
    print("\n[*] Saving model...")
    trainer.save_model()
    
    print("\n[OK] Training complete!")
    print("="*50)

if __name__ == '__main__':
    main()