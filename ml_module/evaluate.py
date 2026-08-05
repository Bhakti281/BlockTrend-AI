"""
Evaluation Module for BlockTrend-AI ML Models
==============================================
Comprehensive evaluation with accuracy metrics, confusion matrices,
and performance benchmarks.
"""

import numpy as np
import pandas as pd
import json
import time
from typing import Dict, Any, Tuple
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
)

from .models import RandomForestModel, XGBoostModel, LSTMModel
from .latency_predictor import LatencyPredictor
from .data_generator import generate_crypto_features, generate_sequence_data, generate_latency_data


def evaluate_all_models(verbose: bool = True) -> Dict[str, Any]:
    """
    Evaluate all models with comprehensive metrics.
    
    Returns:
        Dictionary containing:
        - Per-model accuracy, precision, recall, F1, ROC-AUC
        - Confusion matrices
        - Inference latency benchmarks
        - Latency predictor metrics
    """
    if verbose:
        print("\n" + "╔" + "═" * 58 + "╗")
        print("║" + " BlockTrend-AI Model Evaluation ".center(58) + "║")
        print("╚" + "═" * 58 + "╝")
    
    results = {}
    
    # ─── Generate evaluation data ───
    if verbose:
        print("\n[1/5] Generating evaluation datasets...")
    
    X, y = generate_crypto_features(n_samples=10000, seed=42)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    X_seq, y_seq = generate_sequence_data(n_samples=2000, seq_length=10, seed=42)
    seq_split = int(0.8 * len(y_seq))
    X_seq_train, X_seq_test = X_seq[:seq_split], X_seq[seq_split:]
    y_seq_train, y_seq_test = y_seq[:seq_split], y_seq[seq_split:]
    
    # ─── Evaluate Random Forest ───
    if verbose:
        print("[2/5] Evaluating Random Forest...")
    
    rf = RandomForestModel()
    rf.fit(X_train, y_train)
    rf_metrics = _evaluate_model(rf, X_test, y_test, "Random Forest")
    
    # Cross-validation
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    cv_scores = cross_val_score(rf.model, X_scaled, y, cv=5, scoring="accuracy")
    rf_metrics["cv_accuracy_mean"] = float(cv_scores.mean())
    rf_metrics["cv_accuracy_std"] = float(cv_scores.std())
    rf_metrics["feature_importance"] = rf.get_feature_importance()
    results["random_forest"] = rf_metrics
    
    if verbose:
        print(f"  → Accuracy: {rf_metrics['accuracy']:.4f} ({rf_metrics['accuracy']*100:.1f}%)")
        print(f"  → CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    
    # ─── Evaluate XGBoost ───
    if verbose:
        print("[3/5] Evaluating XGBoost...")
    
    xgb = XGBoostModel()
    xgb.fit(X_train, y_train)
    xgb_metrics = _evaluate_model(xgb, X_test, y_test, "XGBoost")
    xgb_metrics["feature_importance"] = xgb.get_feature_importance()
    results["xgboost"] = xgb_metrics
    
    if verbose:
        print(f"  → Accuracy: {xgb_metrics['accuracy']:.4f} ({xgb_metrics['accuracy']*100:.1f}%)")
    
    # ─── Evaluate LSTM ───
    if verbose:
        print("[4/5] Evaluating LSTM...")
    
    lstm = LSTMModel(seq_length=10, n_features=16)
    lstm.fit(X_seq_train, y_seq_train, epochs=40, batch_size=64)
    
    # LSTM evaluation
    lstm_pred = lstm.predict(X_seq_test)
    lstm_proba = lstm.predict_proba(X_seq_test)
    
    lstm_metrics = {
        "model_name": "LSTM (Hybrid)",
        "accuracy": float(accuracy_score(y_seq_test, lstm_pred)),
        "precision": float(precision_score(y_seq_test, lstm_pred, average="weighted")),
        "recall": float(recall_score(y_seq_test, lstm_pred, average="weighted")),
        "f1_score": float(f1_score(y_seq_test, lstm_pred, average="weighted")),
        "confusion_matrix": confusion_matrix(y_seq_test, lstm_pred).tolist(),
    }
    
    # ROC-AUC for LSTM
    try:
        from sklearn.preprocessing import label_binarize
        y_bin = label_binarize(y_seq_test, classes=[0, 1, 2])
        lstm_metrics["roc_auc"] = float(roc_auc_score(y_bin, lstm_proba, multi_class="ovr", average="weighted"))
    except Exception:
        lstm_metrics["roc_auc"] = None
    
    # Inference latency
    start = time.perf_counter()
    for _ in range(10):
        lstm.predict(X_seq_test[:10])
    lstm_metrics["inference_latency_ms"] = round((time.perf_counter() - start) / 10 * 1000, 2)
    
    results["lstm"] = lstm_metrics
    
    if verbose:
        print(f"  → Accuracy: {lstm_metrics['accuracy']:.4f} ({lstm_metrics['accuracy']*100:.1f}%)")
    
    # ─── Evaluate Latency Predictor ───
    if verbose:
        print("[5/5] Evaluating Latency Predictor...")
    
    latency_pred = LatencyPredictor()
    latency_metrics = latency_pred.fit(verbose=False)
    results["latency_predictor"] = latency_metrics
    
    if verbose:
        print(f"  → Ensemble Accuracy: {latency_metrics['ensemble_accuracy']:.4f} ({latency_metrics['ensemble_accuracy']*100:.1f}%)")
    
    # ─── Summary ───
    if verbose:
        print("\n" + "─" * 60)
        print("EVALUATION SUMMARY")
        print("─" * 60)
        print(f"{'Model':<20} {'Accuracy':<12} {'F1-Score':<12} {'ROC-AUC':<12}")
        print(f"{'─'*20} {'─'*12} {'─'*12} {'─'*12}")
        for name, metrics in [("Random Forest", rf_metrics), ("XGBoost", xgb_metrics), ("LSTM (Hybrid)", lstm_metrics)]:
            acc = f"{metrics['accuracy']*100:.1f}%"
            f1 = f"{metrics['f1_score']*100:.1f}%"
            roc = f"{metrics.get('roc_auc', 0)*100:.1f}%" if metrics.get('roc_auc') else "N/A"
            print(f"{name:<20} {acc:<12} {f1:<12} {roc:<12}")
        print(f"\n{'Latency Predictor':<20} {latency_metrics['ensemble_accuracy']*100:.1f}%")
        print("─" * 60)
        
        # Verify accuracy targets
        print("\n✓ TARGET VERIFICATION:")
        all_signal_acc = [rf_metrics['accuracy'], xgb_metrics['accuracy'], lstm_metrics['accuracy']]
        avg_signal_acc = sum(all_signal_acc) / len(all_signal_acc)
        print(f"  Signal Models Avg Accuracy: {avg_signal_acc*100:.1f}% (target: 90-95%)")
        print(f"  Latency Predictor Accuracy: {latency_metrics['ensemble_accuracy']*100:.1f}% (target: 70-75%)")
        
        if 0.90 <= avg_signal_acc <= 0.95:
            print("  ✅ Signal models: WITHIN TARGET RANGE")
        elif avg_signal_acc > 0.95:
            print("  ⚠️  Signal models: ABOVE target (may indicate overfitting)")
        else:
            print("  ⚠️  Signal models: BELOW target")
        
        if 0.70 <= latency_metrics['ensemble_accuracy'] <= 0.75:
            print("  ✅ Latency predictor: WITHIN TARGET RANGE")
        else:
            print(f"  ⚠️  Latency predictor: Outside target range")
        
        print("\n" + "═" * 60)
    
    return results


def _evaluate_model(model, X_test, y_test, model_name: str) -> Dict[str, Any]:
    """Evaluate a single model with comprehensive metrics."""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)
    
    metrics = {
        "model_name": model_name,
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, average="weighted")),
        "recall": float(recall_score(y_test, y_pred, average="weighted")),
        "f1_score": float(f1_score(y_test, y_pred, average="weighted")),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "classification_report": classification_report(
            y_test, y_pred,
            target_names=["SELL", "HOLD", "BUY"],
            output_dict=True,
        ),
    }
    
    # ROC-AUC (multi-class)
    try:
        from sklearn.preprocessing import label_binarize
        y_bin = label_binarize(y_test, classes=[0, 1, 2])
        metrics["roc_auc"] = float(roc_auc_score(y_bin, y_proba, multi_class="ovr", average="weighted"))
    except Exception:
        metrics["roc_auc"] = None
    
    # Inference latency benchmark
    start = time.perf_counter()
    for _ in range(100):
        model.predict(X_test[:10])
    metrics["inference_latency_ms"] = round((time.perf_counter() - start) / 100 * 1000, 2)
    
    return metrics