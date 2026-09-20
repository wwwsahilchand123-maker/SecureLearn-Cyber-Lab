# ml/train_model.py
"""Train and evaluate the educational phishing classifier."""

import json
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split


class PhishingModelTrainer:
    """Train and evaluate phishing detection model."""

    def __init__(self):
        self.model = None
        self.feature_names = []
        self.metrics = {}

    def create_sample_dataset(self, n_samples=1000):
        """Create a deterministic synthetic dataset for local demos.

        This is intentionally labeled as synthetic data; it must not be treated
        as evidence of real-world model performance.
        """
        rng = np.random.default_rng(42)
        data, labels = [], []

        for _ in range(n_samples):
            is_phishing = int(rng.integers(0, 2))
            if is_phishing:
                feature = {
                    "url_length": rng.integers(50, 200),
                    "num_dots": rng.integers(3, 10),
                    "num_hyphens": rng.integers(2, 8),
                    "num_underscores": rng.integers(1, 5),
                    "num_slashes": rng.integers(3, 10),
                    "num_digits": rng.integers(5, 20),
                    "num_params": rng.integers(2, 10),
                    "has_ip": rng.choice([0, 1], p=[0.3, 0.7]),
                    "has_https": rng.choice([0, 1], p=[0.6, 0.4]),
                    "suspicious_tld": rng.choice([0, 1], p=[0.4, 0.6]),
                    "domain_length": rng.integers(15, 40),
                    "num_subdomains": rng.integers(2, 6),
                    "has_at_symbol": rng.choice([0, 1], p=[0.7, 0.3]),
                    "has_double_slash": rng.choice([0, 1], p=[0.6, 0.4]),
                    "entropy": rng.uniform(3.5, 5.0),
                }
            else:
                feature = {
                    "url_length": rng.integers(10, 60),
                    "num_dots": rng.integers(1, 3),
                    "num_hyphens": rng.integers(0, 2),
                    "num_underscores": rng.integers(0, 1),
                    "num_slashes": rng.integers(1, 4),
                    "num_digits": rng.integers(0, 5),
                    "num_params": rng.integers(0, 3),
                    "has_ip": 0,
                    "has_https": rng.choice([0, 1], p=[0.2, 0.8]),
                    "suspicious_tld": rng.choice([0, 1], p=[0.9, 0.1]),
                    "domain_length": rng.integers(5, 20),
                    "num_subdomains": rng.integers(0, 2),
                    "has_at_symbol": 0,
                    "has_double_slash": 0,
                    "entropy": rng.uniform(2.0, 3.5),
                }
            data.append(feature)
            labels.append(is_phishing)

        df = pd.DataFrame(data)
        df["label"] = labels
        return df

    def train(self, df):
        """Train the model and report multiple evaluation metrics."""
        if "label" not in df.columns:
            raise ValueError("Dataset must contain a 'label' column")
        if df["label"].nunique() < 2:
            raise ValueError("Dataset must contain both classes")

        X = df.drop("label", axis=1)
        y = df["label"]
        self.feature_names = X.columns.tolist()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        self.model = RandomForestClassifier(
            n_estimators=100, max_depth=10, random_state=42, n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)

        self.metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1_score": f1_score(y_test, y_pred, zero_division=0),
            "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
            "test_samples": len(y_test),
        }
        return self.metrics

    def save_model(self, model_path="ml/model/phishing_model.pkl", metrics_path="ml/model/metrics.json"):
        """Save trained model and evaluation metadata."""
        if self.model is None:
            raise RuntimeError("Train the model before saving it")
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump({"model": self.model, "feature_names": self.feature_names}, model_path)
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(self.metrics, f, indent=2)

    def get_feature_importance(self):
        if self.model is None:
            return None
        return dict(sorted(
            zip(self.feature_names, self.model.feature_importances_),
            key=lambda item: item[1],
            reverse=True,
        ))


def main():
    trainer = PhishingModelTrainer()
    df = trainer.create_sample_dataset(n_samples=2000)
    dataset_path = "ml/dataset/phishing_data.csv"
    os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
    df.to_csv(dataset_path, index=False)
    trainer.train(df)
    trainer.save_model()


if __name__ == "__main__":
    main()
