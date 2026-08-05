#!/usr/bin/env python3
"""
BlockTrend-AI ML Pipeline Runner
==================================
Run this script to train and evaluate all ML models.

Usage:
    python -m ml_module.run_pipeline [--train] [--evaluate] [--all]
"""

import argparse
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_module.train import train_all_models
from ml_module.evaluate import evaluate_all_models
from ml_module.latency_predictor import LatencyPredictor


def main():
    parser = argparse.ArgumentParser(description="BlockTrend-AI ML Pipeline")
    parser.add_argument("--train", action="store_true", help="Train all models")
    parser.add_argument("--evaluate", action="store_true", help="Evaluate all models")
    parser.add_argument("--latency-check", action="store_true", help="Run live latency check")
    parser.add_argument("--all", action="store_true", help="Run full pipeline (train + evaluate)")
    
    args = parser.parse_args()
    
    # Default to --all if no args provided
    if not any([args.train, args.evaluate, args.latency_check, args.all]):
        args.all = True
    
    if args.all or args.train:
        print("\n🚀 Starting model training...")
        train_all_models(verbose=True)
    
    if args.all or args.evaluate:
        print("\n📊 Starting model evaluation...")
        results = evaluate_all_models(verbose=True)
    
    if args.all or args.latency_check:
        print("\n⚡ Running live latency check...")
        predictor = LatencyPredictor()
        predictor.fit(verbose=True)
        live_results = predictor.run_live_latency_check()
        
        print("\n─── Live Latency Results ───")
        for r in live_results["results"]:
            status_icon = "🟢" if r["latency_ms"] and r["latency_ms"] < 200 else "🟡" if r["latency_ms"] and r["latency_ms"] < 500 else "🔴"
            latency_str = f"{r['latency_ms']}ms" if r["latency_ms"] else "N/A"
            pred_str = r.get("predicted_category", "N/A")
            print(f"  {status_icon} {r['endpoint']:<20} {latency_str:<10} (actual: {r['actual_category']}, predicted: {pred_str})")
        
        if live_results["summary"]["avg_latency_ms"]:
            print(f"\n  ⚡ Average: {live_results['summary']['avg_latency_ms']}ms")


if __name__ == "__main__":
    main()