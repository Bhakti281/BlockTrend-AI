"""AI Signals page — ML ensemble predictions with SHAP-explained feature importance."""

import streamlit as st
import pandas as pd


SIGNALS = [
    {
        "coin": "Bitcoin",
        "symbol": "BTC",
        "action": "BUY",
        "confidence": 87,
        "expected_change": 4.2,
        "models": [
            {"name": "Random Forest", "vote": "BUY", "weight": 0.79},
            {"name": "XGBoost", "vote": "BUY", "weight": 0.83},
            {"name": "LSTM (24h)", "vote": "BUY", "weight": 0.87},
        ],
        "features": [
            {"name": "MACD Crossover", "impact": 0.32, "direction": "positive"},
            {"name": "RSI Momentum", "impact": 0.24, "direction": "positive"},
            {"name": "Volume Surge", "impact": 0.18, "direction": "positive"},
            {"name": "Sentiment Score", "impact": 0.15, "direction": "positive"},
            {"name": "Bollinger Width", "impact": 0.11, "direction": "negative"},
        ],
    },
    {
        "coin": "Ethereum",
        "symbol": "ETH",
        "action": "BUY",
        "confidence": 74,
        "expected_change": 2.8,
        "models": [
            {"name": "Random Forest", "vote": "BUY", "weight": 0.72},
            {"name": "XGBoost", "vote": "BUY", "weight": 0.76},
            {"name": "LSTM (24h)", "vote": "BUY", "weight": 0.74},
        ],
        "features": [
            {"name": "EMA Crossover", "impact": 0.28, "direction": "positive"},
            {"name": "DeFi TVL Growth", "impact": 0.22, "direction": "positive"},
            {"name": "Gas Fee Decline", "impact": 0.19, "direction": "positive"},
            {"name": "Whale Activity", "impact": 0.17, "direction": "positive"},
            {"name": "Correlation BTC", "impact": 0.14, "direction": "negative"},
        ],
    },
    {
        "coin": "Solana",
        "symbol": "SOL",
        "action": "HOLD",
        "confidence": 62,
        "expected_change": 0.8,
        "models": [
            {"name": "Random Forest", "vote": "HOLD", "weight": 0.61},
            {"name": "XGBoost", "vote": "BUY", "weight": 0.65},
            {"name": "LSTM (24h)", "vote": "HOLD", "weight": 0.60},
        ],
        "features": [
            {"name": "Network Activity", "impact": 0.25, "direction": "positive"},
            {"name": "RSI Neutral", "impact": 0.20, "direction": "negative"},
            {"name": "Volume Flat", "impact": 0.18, "direction": "negative"},
            {"name": "Dev Activity", "impact": 0.22, "direction": "positive"},
            {"name": "Market Correlation", "impact": 0.15, "direction": "negative"},
        ],
    },
    {
        "coin": "Cardano",
        "symbol": "ADA",
        "action": "SELL",
        "confidence": 68,
        "expected_change": -2.1,
        "models": [
            {"name": "Random Forest", "vote": "SELL", "weight": 0.66},
            {"name": "XGBoost", "vote": "SELL", "weight": 0.70},
            {"name": "LSTM (24h)", "vote": "SELL", "weight": 0.68},
        ],
        "features": [
            {"name": "Bearish Divergence", "impact": 0.30, "direction": "negative"},
            {"name": "Volume Decline", "impact": 0.25, "direction": "negative"},
            {"name": "Support Break", "impact": 0.20, "direction": "negative"},
            {"name": "Sentiment Drop", "impact": 0.15, "direction": "negative"},
            {"name": "Staking Outflow", "impact": 0.10, "direction": "negative"},
        ],
    },
]


def render():
    st.markdown('<h1 class="main-header">AI Signals</h1>', unsafe_allow_html=True)
    st.markdown("ML ensemble predictions with SHAP-explained feature importance for each signal.")
    st.divider()

    cols = st.columns(2)
    for i, signal in enumerate(SIGNALS):
        with cols[i % 2]:
            render_signal_card(signal)


def render_signal_card(signal: dict):
    action = signal["action"]
    badge_class = f"signal-{action.lower()}"
    change_color = "bull" if signal["expected_change"] >= 0 else "bear"
    change_arrow = "↑" if signal["expected_change"] >= 0 else "↓"

    st.markdown(f"""
    <div class="glass-card" style="margin-bottom:1rem;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
            <strong style="font-family:'Sora';font-size:1.1rem;">🧠 {signal['coin']} ({signal['symbol']})</strong>
            <span class="signal-badge {badge_class}">{action} · {signal['confidence']}%</span>
        </div>
        <div class="{change_color}" style="font-size:0.85rem;margin-bottom:1rem;">
            {change_arrow} {signal['expected_change']:+.1f}% expected (24h)
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Model votes
    with st.expander(f"📊 Model Votes — {signal['symbol']}", expanded=False):
        df = pd.DataFrame(signal["models"])
        df.columns = ["Model", "Vote", "Confidence"]
        df["Confidence"] = df["Confidence"].apply(lambda x: f"{x*100:.0f}%")
        st.dataframe(df, use_container_width=True, hide_index=True)

    # SHAP features
    with st.expander(f"🔍 SHAP Features — {signal['symbol']}", expanded=False):
        for feat in signal["features"]:
            color = "#22c55e" if feat["direction"] == "positive" else "#ef4444"
            sign = "+" if feat["direction"] == "positive" else "-"
            bar_width = int(feat["impact"] * 300)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                <span style="flex:1;font-size:0.8rem;color:#9ca3af;">{feat['name']}</span>
                <div style="width:100px;height:8px;background:#1e293b;border-radius:4px;overflow:hidden;">
                    <div style="width:{bar_width}%;height:100%;background:{color};border-radius:4px;"></div>
                </div>
                <span style="font-family:'JetBrains Mono';font-size:0.75rem;color:{color};width:40px;text-align:right;">
                    {sign}{feat['impact']*100:.0f}%
                </span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")