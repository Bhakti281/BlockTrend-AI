"""
BlockTrend-AI ML Module
=======================
Machine Learning models for cryptocurrency price prediction.
Includes Random Forest, XGBoost, and LSTM ensemble with latency prediction.
"""

from .models import RandomForestModel, XGBoostModel, LSTMModel, LSTMNet
from .ensemble import EnsemblePredictor
from .latency_predictor import LatencyPredictor
from .data_generator import generate_crypto_features
from .train import train_all_models
from .evaluate import evaluate_all_models

__version__ = "1.0.0"
__all__ = [
    "RandomForestModel",
    "XGBoostModel",
    "LSTMModel",
    "EnsemblePredictor",
    "LatencyPredictor",
    "generate_crypto_features",
    "train_all_models",
    "evaluate_all_models",
]