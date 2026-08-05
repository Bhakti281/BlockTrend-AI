"""
Training Script for BlockTrend-AI ML Models
=============================================
Trains all models and saves them to the models/ directory.
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, Any

from .ensemble import EnsemblePredictor
from .latency_predictor import LatencyPredictor


def train_all_models(
    save_dir: str = "ml_module/saved_models",
    verbose: bool = True,
) -> Dict[str, Any]:
    """
    Train all ML models (ensemble + latency predictor).
    
    Args:
        save_dir: Directory to save trained models.
        verbose: Print training progress.
        
    Returns:
        Dictionary with training results and metrics.
    """
    start_time = time.time()
    
    if verbose:
        print("\n" + "╔" + "═" * 58 + "╗")
        print("║" + " BlockTrend-AI ML Training Pipeline ".center(58) + "║")
        print("╚" + "═" * 58 + "╝")
        print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Save directory: {save_dir}")
    
    results = {}
    
    # ─── Train Ensemble (RF + XGBoost + LSTM) ───
    ensemble = EnsemblePredictor()
    ensemble_metrics = ensemble.fit(verbose=verbose)
    results["ensemble"] = ensemble_metrics
    
    # Save ensemble models
    ensemble.save(save_dir)
    if verbose:
        print(f"\n✓ Ensemble models saved to {save_dir}/")
    
    # ─── Train Latency Predictor ───
    latency_pred = LatencyPredictor()
    latency_metrics = latency_pred.fit(verbose=verbose)
    results["latency"] = latency_metrics
    
    # Calculate total time
    total_time = time.time() - start_time
    results["training_time_seconds"] = round(total_time, 2)
    results["timestamp"] = datetime.now().isoformat()
    
    # Save training report
    os.makedirs(save_dir, exist_ok=True)
    report_path = os.path.join(save_dir, "training_report.json")
    
    # Make report JSON serializable
    serializable_results = _make_serializable(results)
    with open(report_path, "w") as f:
        json.dump(serializable_results, f, indent=2)
    
    if verbose:
        print(f"\n{'─' * 60}")
        print(f"Total training time: {total_time:.1f}s")
        print(f"Training report saved: {report_path}")
        print(f"{'─' * 60}\n")
    
    return results


def _make_serializable(obj):
    """Convert numpy types to Python native types for JSON serialization."""
    import numpy as np
    
    if isinstance(obj, dict):
        return {k: _make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_make_serializable(item) for item in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj