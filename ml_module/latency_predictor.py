"""
Latency Predictor for BlockTrend-AI
=====================================
Predicts API response latency categories using an ensemble approach.
Target accuracy: 70-75% (realistic for network latency prediction).
"""

import numpy as np
import pandas as pd
import time
import requests
from typing import Dict, List, Tuple, Optional
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from .data_generator import generate_latency_data


class LatencyPredictor:
    """
    Predicts API latency categories:
    - 0: Excellent (< 200ms)
    - 1: Good (200-500ms)  
    - 2: Slow (> 500ms)
    
    Uses a Random Forest + Gradient Boosting ensemble.
    Designed for 70-75% accuracy reflecting real-world latency unpredictability.
    """
    
    CATEGORY_MAP = {0: "Excellent", 1: "Good", 2: "Slow"}
    CATEGORY_THRESHOLDS = {"Excellent": 200, "Good": 500}
    
    ENDPOINTS = [
        {"label": "CoinGecko Markets", "url": "https://api.coingecko.com/api/v3/ping"},
        {"label": "Binance Ticker", "url": "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"},
        {"label": "CryptoCompare", "url": "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD"},
    ]
    
    def __init__(self):
        self.rf_model = RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1,
        )
        self.gb_model = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            random_state=42,
        )
        self.scaler = StandardScaler()
        self.is_fitted = False
        self.metrics = {}
    
    def fit(self, verbose: bool = True) -> Dict[str, float]:
        """
        Train the latency prediction model.
        
        Returns:
            Dictionary with accuracy and per-class metrics.
        """
        if verbose:
            print("\n" + "=" * 60)
            print("Latency Predictor Training")
            print("=" * 60)
            print("\n[1/3] Generating latency training data...")
        
        X, y = generate_latency_data(n_samples=5000, seed=42)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        if verbose:
            print("[2/3] Training Random Forest + Gradient Boosting ensemble...")
        
        # Train models
        self.rf_model.fit(X_train_scaled, y_train)
        self.gb_model.fit(X_train_scaled, y_train)
        
        # Evaluate
        rf_pred = self.rf_model.predict(X_test_scaled)
        gb_pred = self.gb_model.predict(X_test_scaled)
        
        # Ensemble prediction (average probabilities)
        rf_proba = self.rf_model.predict_proba(X_test_scaled)
        gb_proba = self.gb_model.predict_proba(X_test_scaled)
        ensemble_proba = 0.5 * rf_proba + 0.5 * gb_proba
        ensemble_pred = np.argmax(ensemble_proba, axis=1)
        
        # Calculate metrics
        rf_acc = accuracy_score(y_test, rf_pred)
        gb_acc = accuracy_score(y_test, gb_pred)
        ensemble_acc = accuracy_score(y_test, ensemble_pred)
        
        self.metrics = {
            "rf_accuracy": float(rf_acc),
            "gb_accuracy": float(gb_acc),
            "ensemble_accuracy": float(ensemble_acc),
            "classification_report": classification_report(
                y_test, ensemble_pred,
                target_names=["Excellent", "Good", "Slow"],
                output_dict=True,
            ),
        }
        
        self.is_fitted = True
        
        if verbose:
            print(f"[3/3] Evaluation complete!")
            print(f"\n  Random Forest Accuracy:  {rf_acc:.4f} ({rf_acc*100:.1f}%)")
            print(f"  Gradient Boosting Acc:   {gb_acc:.4f} ({gb_acc*100:.1f}%)")
            print(f"  Ensemble Accuracy:       {ensemble_acc:.4f} ({ensemble_acc*100:.1f}%)")
            print(f"\n{'=' * 60}")
        
        return self.metrics
    
    def predict_latency_category(self, features: pd.DataFrame) -> List[Dict]:
        """
        Predict latency category for given conditions.
        
        Args:
            features: DataFrame with columns matching training features.
            
        Returns:
            List of prediction dictionaries.
        """
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        
        X_scaled = self.scaler.transform(features)
        rf_proba = self.rf_model.predict_proba(X_scaled)
        gb_proba = self.gb_model.predict_proba(X_scaled)
        ensemble_proba = 0.5 * rf_proba + 0.5 * gb_proba
        predictions = np.argmax(ensemble_proba, axis=1)
        confidences = np.max(ensemble_proba, axis=1)
        
        results = []
        for i in range(len(features)):
            results.append({
                "predicted_category": self.CATEGORY_MAP[predictions[i]],
                "confidence": float(confidences[i]),
                "probabilities": {
                    "Excellent": float(ensemble_proba[i][0]),
                    "Good": float(ensemble_proba[i][1]),
                    "Slow": float(ensemble_proba[i][2]),
                },
            })
        
        return results
    
    def run_live_latency_check(self) -> Dict[str, any]:
        """
        Run live latency measurements against crypto API endpoints
        and predict their categories.
        
        Returns:
            Dictionary with measured latencies and predictions.
        """
        results = []
        
        for endpoint in self.ENDPOINTS:
            try:
                start = time.perf_counter()
                resp = requests.get(endpoint["url"], timeout=10)
                latency_ms = round((time.perf_counter() - start) * 1000)
                
                # Determine actual category
                if latency_ms < 200:
                    actual_category = "Excellent"
                elif latency_ms < 500:
                    actual_category = "Good"
                else:
                    actual_category = "Slow"
                
                results.append({
                    "endpoint": endpoint["label"],
                    "latency_ms": latency_ms,
                    "status": "success",
                    "status_code": resp.status_code,
                    "actual_category": actual_category,
                })
            except requests.Timeout:
                results.append({
                    "endpoint": endpoint["label"],
                    "latency_ms": None,
                    "status": "timeout",
                    "status_code": None,
                    "actual_category": "Slow",
                })
            except Exception as e:
                results.append({
                    "endpoint": endpoint["label"],
                    "latency_ms": None,
                    "status": "error",
                    "status_code": None,
                    "actual_category": "Slow",
                })
        
        # Generate prediction features for current conditions
        from datetime import datetime
        now = datetime.now()
        
        if self.is_fitted:
            for i, result in enumerate(results):
                features = pd.DataFrame([{
                    "hour_of_day": now.hour,
                    "day_of_week": now.weekday(),
                    "concurrent_requests": np.random.exponential(30),
                    "payload_size_kb": np.random.exponential(5),
                    "endpoint_type": i % 4,
                    "network_congestion": np.random.beta(2, 5),
                    "server_load": np.random.beta(3, 3),
                    "region_distance": np.random.uniform(0.2, 0.8),
                    "cache_hit": 1.0 if result.get("latency_ms") and result["latency_ms"] < 100 else 0.0,
                    "retry_count": 0.0,
                }])
                
                prediction = self.predict_latency_category(features)[0]
                result["predicted_category"] = prediction["predicted_category"]
                result["prediction_confidence"] = prediction["confidence"]
        
        # Calculate summary
        valid_latencies = [r["latency_ms"] for r in results if r["latency_ms"] is not None]
        summary = {
            "avg_latency_ms": round(sum(valid_latencies) / len(valid_latencies)) if valid_latencies else None,
            "min_latency_ms": min(valid_latencies) if valid_latencies else None,
            "max_latency_ms": max(valid_latencies) if valid_latencies else None,
            "endpoints_tested": len(results),
            "endpoints_success": sum(1 for r in results if r["status"] == "success"),
        }
        
        return {"results": results, "summary": summary}