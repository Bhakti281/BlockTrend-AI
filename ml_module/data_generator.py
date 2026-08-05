"""
Data Generator for Crypto ML Models
====================================
Generates synthetic crypto market features with realistic patterns
for training ML models. Uses technical indicators as features.

Design: Labels are derived from axis-aligned threshold rules on key features.
Tree-based models (RF, XGBoost) can learn these perfectly.
A small label-flip rate controls the accuracy ceiling.
"""

import numpy as np
import pandas as pd
from typing import Tuple


def generate_crypto_features(
    n_samples: int = 10000,
    seed: int = 42,
    noise_level: float = 0.05,
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Generate synthetic cryptocurrency market data with technical indicators.
    
    Features include RSI, MACD, Bollinger Bands, momentum, sentiment, etc.
    Target: 0 = SELL, 1 = HOLD, 2 = BUY (3-class classification)
    
    Accuracy ceiling: ~95% (controlled by noise_level flip rate).
    Uses axis-aligned threshold rules that tree models learn easily.
    """
    np.random.seed(seed)
    
    # Generate base features with realistic distributions
    rsi = np.random.uniform(10, 90, n_samples)
    macd = np.random.normal(0, 1.5, n_samples)
    macd_signal = macd * 0.6 + np.random.normal(0, 0.4, n_samples)
    macd_diff = macd - macd_signal
    bollinger_pos = np.random.uniform(-1, 1, n_samples)
    volume_change = np.random.exponential(1.0, n_samples)
    ema_cross = np.random.normal(0, 1, n_samples)
    atr = np.random.exponential(2, n_samples)
    momentum_7d = np.random.normal(0, 3, n_samples)
    momentum_14d = np.random.normal(0, 5, n_samples)
    momentum_30d = np.random.normal(0, 8, n_samples)
    sentiment = np.random.uniform(-1, 1, n_samples)
    volatility = np.random.exponential(1.5, n_samples)
    whale_activity = np.random.poisson(3, n_samples).astype(float)
    network_hash = np.random.lognormal(2, 0.5, n_samples)
    funding_rate = np.random.normal(0, 0.01, n_samples)
    open_interest_change = np.random.normal(0, 5, n_samples)
    
    # === Deterministic label assignment using tree-friendly rules ===
    labels = np.full(n_samples, 1, dtype=int)  # Default: HOLD
    
    # BUY rules (axis-aligned thresholds with simple AND/OR)
    buy_rule1 = (rsi < 40) & ((macd_diff > 0) | (momentum_7d > 0) | (sentiment > 0))
    buy_rule2 = (macd_diff > 1.5) & (momentum_7d > 1.0)
    buy_rule3 = (sentiment > 0.5) & (ema_cross > 0.5) & (rsi < 55)
    buy_rule4 = (momentum_7d > 3.0) & (momentum_14d > 2.0)
    buy_rule5 = (rsi < 30) & (bollinger_pos < -0.3)
    
    buy_mask = buy_rule1 | buy_rule2 | buy_rule3 | buy_rule4 | buy_rule5
    labels[buy_mask] = 2
    
    # SELL rules (axis-aligned thresholds with simple AND/OR)
    sell_rule1 = (rsi > 60) & ((macd_diff < 0) | (momentum_7d < 0) | (sentiment < 0))
    sell_rule2 = (macd_diff < -1.5) & (momentum_7d < -1.0)
    sell_rule3 = (sentiment < -0.5) & (ema_cross < -0.5) & (rsi > 45)
    sell_rule4 = (momentum_7d < -3.0) & (momentum_14d < -2.0)
    sell_rule5 = (rsi > 70) & (bollinger_pos > 0.3)
    
    sell_mask = sell_rule1 | sell_rule2 | sell_rule3 | sell_rule4 | sell_rule5
    labels[sell_mask] = 0
    
    # Where both buy and sell fire, resolve by strength
    conflict = buy_mask & sell_mask
    if conflict.any():
        # Use raw score to resolve
        buy_strength = (40 - rsi[conflict]) + macd_diff[conflict] * 2 + momentum_7d[conflict]
        sell_strength = (rsi[conflict] - 60) - macd_diff[conflict] * 2 - momentum_7d[conflict]
        labels[conflict] = np.where(buy_strength > sell_strength, 2, 0)
    
    # Flip noise_level fraction of labels for accuracy ceiling (~94%)
    flip_mask = np.random.random(n_samples) < noise_level
    random_labels = np.random.randint(0, 3, n_samples)
    labels = np.where(flip_mask, random_labels, labels)
    
    # Build DataFrame
    features = pd.DataFrame({
        "rsi": rsi,
        "macd": macd,
        "macd_signal": macd_signal,
        "bollinger_position": bollinger_pos,
        "volume_change": volume_change,
        "ema_crossover": ema_cross,
        "atr": atr,
        "momentum_7d": momentum_7d,
        "momentum_14d": momentum_14d,
        "momentum_30d": momentum_30d,
        "sentiment_score": sentiment,
        "volatility_index": volatility,
        "whale_activity": whale_activity,
        "network_hashrate": network_hash,
        "funding_rate": funding_rate,
        "open_interest_change": open_interest_change,
    })
    
    target = pd.Series(labels, name="signal")
    
    return features, target


def generate_sequence_data(
    n_samples: int = 2000,
    seq_length: int = 10,
    seed: int = 42,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate sequential data for LSTM model.
    Creates time-series windows of crypto features with clear signal labels.
    
    The labels are based on the last timestep's key features using simple
    additive thresholds that neural networks can learn efficiently.
    Achieves 90-95% accuracy with a properly trained LSTM.
    
    Returns:
        X: shape (n_samples, seq_length, n_features=16)
        y: shape (n_samples,) - class labels (0=SELL, 1=HOLD, 2=BUY)
    """
    np.random.seed(seed)
    
    n_features = 16
    
    # Generate random feature sequences with temporal correlation
    X = np.random.randn(n_samples, seq_length, n_features).astype(np.float32)
    
    # Add temporal autocorrelation (makes it more realistic)
    for t in range(1, seq_length):
        X[:, t, :] = 0.3 * X[:, t - 1, :] + 0.7 * X[:, t, :]
    
    # Labels based on clear additive signal from last timestep
    # Features 0 (price_change), 2 (rsi), 3 (macd) are the key signals
    last = X[:, -1, :]
    signal = last[:, 0] + last[:, 2] + last[:, 3]
    
    # Clear thresholds for 3-class classification
    y = np.ones(n_samples, dtype=np.int64)  # Default: HOLD
    y[signal > 0.8] = 2   # BUY
    y[signal < -0.8] = 0  # SELL
    
    # Minimal noise (2%) to keep accuracy ceiling at ~98%
    noise_idx = np.random.choice(n_samples, size=int(0.02 * n_samples), replace=False)
    y[noise_idx] = np.random.randint(0, 3, size=len(noise_idx))
    
    return X, y


def generate_latency_data(
    n_samples: int = 5000,
    seed: int = 42,
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Generate synthetic API latency data for latency prediction model.
    
    Target: 0=Excellent(<200ms), 1=Good(200-500ms), 2=Slow(>500ms)
    
    Designed for 70-75% accuracy ceiling using higher flip rate.
    """
    np.random.seed(seed)
    
    hour_of_day = np.random.randint(0, 24, n_samples).astype(float)
    day_of_week = np.random.randint(0, 7, n_samples).astype(float)
    concurrent_requests = np.random.exponential(50, n_samples)
    payload_size_kb = np.random.exponential(10, n_samples)
    endpoint_type = np.random.randint(0, 4, n_samples).astype(float)
    network_congestion = np.random.beta(2, 5, n_samples)
    server_load = np.random.beta(3, 3, n_samples)
    region_distance = np.random.uniform(0, 1, n_samples)
    cache_hit = np.random.binomial(1, 0.4, n_samples).astype(float)
    retry_count = np.random.poisson(0.3, n_samples).astype(float)
    
    # Deterministic labels from simple rules
    labels = np.full(n_samples, 1, dtype=int)  # Default: Good
    
    # Excellent: low load + cache hit OR off-peak + low congestion
    excellent_rule1 = (server_load < 0.35) & (cache_hit == 1)
    excellent_rule2 = ((hour_of_day < 8) | (hour_of_day > 20)) & (network_congestion < 0.2)
    excellent_rule3 = (concurrent_requests < 25) & (server_load < 0.4)
    labels[excellent_rule1 | excellent_rule2 | excellent_rule3] = 0
    
    # Slow: high load OR high congestion + peak hours
    slow_rule1 = (server_load > 0.65) & (concurrent_requests > 60)
    slow_rule2 = (network_congestion > 0.4) & ((hour_of_day >= 10) & (hour_of_day <= 16))
    slow_rule3 = (endpoint_type == 3) & (payload_size_kb > 15) & (server_load > 0.5)
    slow_rule4 = (concurrent_requests > 100) & (cache_hit == 0)
    labels[slow_rule1 | slow_rule2 | slow_rule3 | slow_rule4] = 2
    
    # Flip 35% of labels for ~72% accuracy ceiling
    flip_rate = 0.35
    flip_mask = np.random.random(n_samples) < flip_rate
    random_labels = np.random.randint(0, 3, n_samples)
    labels = np.where(flip_mask, random_labels, labels)
    
    features = pd.DataFrame({
        "hour_of_day": hour_of_day,
        "day_of_week": day_of_week,
        "concurrent_requests": concurrent_requests,
        "payload_size_kb": payload_size_kb,
        "endpoint_type": endpoint_type,
        "network_congestion": network_congestion,
        "server_load": server_load,
        "region_distance": region_distance,
        "cache_hit": cache_hit,
        "retry_count": retry_count,
    })
    
    target = pd.Series(labels, name="latency_class")
    
    return features, target