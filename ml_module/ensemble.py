"""
Ensemble Predictor for BlockTrend-AI
=====================================
Combines Random Forest, XGBoost, and LSTM predictions
using weighted voting for final signal generation.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any

from .models import RandomForestModel, XGBoostModel, LSTMModel
from .data_generator import generate_crypto_features, generate_sequence_data


class EnsemblePredictor:
    """
    Ensemble model combining RF, XGBoost, and LSTM with weighted voting.
    
    Weights are assigned based on individual model performance:
    - LSTM: 0.40 (best at capturing temporal patterns)
    - XGBoost: 0.35 (strong gradient boosting)
    - Random Forest: 0.25 (robust baseline)
    """
    
    SIGNAL_MAP = {0: "SELL", 1: "HOLD", 2: "BUY"}
    
    def __init__(
        self,
        rf_weight: float = 0.25,
        xgb_weight: float = 0.35,
        lstm_weight: float = 0.40,
    ):
        self.rf_model = RandomForestModel()
        self.xgb_model = XGBoostModel()
        self.lstm_model = LSTMModel()
        
        # Normalize weights
        total = rf_weight + xgb_weight + lstm_weight
        self.rf_weight = rf_weight / total
        self.xgb_weight = xgb_weight / total
        self.lstm_weight = lstm_weight / total
        
        self.is_fitted = False
        self.training_metrics = {}
    
    def fit(self, verbose: bool = True) -> Dict[str, Any]:
        """
        Train all models in the ensemble.
        
        Returns:
            Dictionary with training metrics for each model.
        """
        if verbose:
            print("=" * 60)
            print("BlockTrend-AI Ensemble Training")
            print("=" * 60)
        
        # Generate training data
        if verbose:
            print("\n[1/4] Generating training data...")
        X_tabular, y_tabular = generate_crypto_features(n_samples=10000, seed=42)
        X_seq, y_seq = generate_sequence_data(n_samples=2000, seq_length=10, seed=42)
        
        # Train Random Forest
        if verbose:
            print("[2/4] Training Random Forest (500 trees, all features)...")
        self.rf_model.fit(X_tabular, y_tabular)
        
        # Train XGBoost
        if verbose:
            print("[3/4] Training XGBoost (300 rounds, depth=8, lr=0.1)...")
        self.xgb_model.fit(X_tabular, y_tabular)
        
        # Train LSTM
        if verbose:
            print("[4/4] Training Hybrid LSTM (64 units, 10-step sequences)...")
        lstm_history = self.lstm_model.fit(
            X_seq, y_seq,
            epochs=40,
            batch_size=64,
            validation_split=0.15,
        )
        
        self.is_fitted = True
        
        if verbose:
            print("\n✓ All models trained successfully!")
            print("=" * 60)
        
        return {
            "rf_feature_importance": self.rf_model.get_feature_importance(),
            "xgb_feature_importance": self.xgb_model.get_feature_importance(),
            "lstm_final_val_accuracy": lstm_history.get("val_accuracy", [0])[-1],
        }
    
    def predict(self, X_tabular: pd.DataFrame, X_sequential: Optional[np.ndarray] = None) -> Dict[str, any]:
        """
        Generate ensemble prediction.
        
        Args:
            X_tabular: DataFrame with feature columns for RF and XGBoost
            X_sequential: Optional sequential data for LSTM. If None, uses tabular features.
            
        Returns:
            Dictionary with prediction details including individual model votes.
        """
        if not self.is_fitted:
            raise ValueError("Ensemble not fitted. Call fit() first.")
        
        # Get probabilities from each model
        rf_proba = self.rf_model.predict_proba(X_tabular)
        xgb_proba = self.xgb_model.predict_proba(X_tabular)
        
        if X_sequential is not None:
            lstm_proba = self.lstm_model.predict_proba(X_sequential)
        else:
            # Create pseudo-sequence from tabular data (repeat for sequence length)
            seq_data = np.tile(X_tabular.values, (1, 1)).reshape(
                len(X_tabular), 1, X_tabular.shape[1]
            )
            seq_data = np.repeat(seq_data, 24, axis=1)
            lstm_proba = self.lstm_model.predict_proba(seq_data)
        
        # Weighted ensemble
        ensemble_proba = (
            self.rf_weight * rf_proba +
            self.xgb_weight * xgb_proba +
            self.lstm_weight * lstm_proba
        )
        
        ensemble_pred = np.argmax(ensemble_proba, axis=1)
        confidence = np.max(ensemble_proba, axis=1)
        
        # Individual model predictions
        rf_pred = np.argmax(rf_proba, axis=1)
        xgb_pred = np.argmax(xgb_proba, axis=1)
        lstm_pred = np.argmax(lstm_proba, axis=1)
        
        results = []
        for i in range(len(X_tabular)):
            results.append({
                "ensemble_signal": self.SIGNAL_MAP[ensemble_pred[i]],
                "confidence": float(confidence[i]),
                "models": [
                    {"name": "Random Forest", "vote": self.SIGNAL_MAP[rf_pred[i]], "weight": self.rf_weight, "confidence": float(np.max(rf_proba[i]))},
                    {"name": "XGBoost", "vote": self.SIGNAL_MAP[xgb_pred[i]], "weight": self.xgb_weight, "confidence": float(np.max(xgb_proba[i]))},
                    {"name": "LSTM (24h)", "vote": self.SIGNAL_MAP[lstm_pred[i]], "weight": self.lstm_weight, "confidence": float(np.max(lstm_proba[i]))},
                ],
                "probabilities": {
                    "SELL": float(ensemble_proba[i][0]),
                    "HOLD": float(ensemble_proba[i][1]),
                    "BUY": float(ensemble_proba[i][2]),
                },
            })
        
        return results if len(results) > 1 else results[0]
    
    def save(self, directory: str) -> None:
        """Save all models to directory."""
        import os
        os.makedirs(directory, exist_ok=True)
        self.rf_model.save(os.path.join(directory, "random_forest.pkl"))
        self.xgb_model.save(os.path.join(directory, "xgboost.pkl"))
        self.lstm_model.save(os.path.join(directory, "lstm"))
    
    def load(self, directory: str) -> "EnsemblePredictor":
        """Load all models from directory."""
        import os
        self.rf_model.load(os.path.join(directory, "random_forest.pkl"))
        self.xgb_model.load(os.path.join(directory, "xgboost.pkl"))
        self.lstm_model.load(os.path.join(directory, "lstm"))
        self.is_fitted = True
        return self