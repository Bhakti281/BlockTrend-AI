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
    st.markdown('<p class="sub-header">ML ensemble predictions with SHAP-explained feature importance for each signal.</p>', unsafe_allow_html=True)
    st.divider()

    # Summary metrics
    buy_count = sum(1 for s in SIGNALS if s["action"] == "BUY")
    sell_count = sum(1 for s in SIGNALS if s["action"] == "SELL")
    hold_count = sum(1 for s in SIGNALS if s["action"] == "HOLD")
    avg_conf = sum(s["confidence"] for s in SIGNALS) / len(SIGNALS)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <div class="metric-label">Buy Signals</div>
            <div class="metric-value bull">{buy_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <div class="metric-label">Sell Signals</div>
            <div class="metric-value bear">{sell_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <div class="metric-label">Hold Signals</div>
            <div class="metric-value" style="color:#9ca3af;">{hold_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <div class="metric-label">Avg Confidence</div>
            <div class="metric-value cyan">{avg_conf:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(2)
    for i, signal in enumerate(SIGNALS):
        with cols[i % 2]:
            render_signal_card(signal)


def render_signal_card(signal: dict):
    action = signal["action"]
    badge_class = f"signal-{action.lower()}"
    change_color = "bull" if signal["expected_change"] >= 0 else "bear"
    change_arrow = "▲" if signal["expected_change"] >= 0 else "▼"

    st.markdown(f"""
    <div class="glass-card" style="margin-bottom:1.25rem;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
            <div>
                <span style="font-family:'Sora';font-size:1.1rem;font-weight:600;color:#f1f5f9;">{signal['coin']}</span>
                <span style="color:#64748b;font-size:0.85rem;margin-left:0.5rem;">{signal['symbol']}</span>
            </div>
            <span class="signal-badge {badge_class}">{action} · {signal['confidence']}%</span>
        </div>
        <div class="{change_color}" style="font-size:0.85rem;margin-bottom:0.75rem;">
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
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                <span style="flex:1;font-size:0.8rem;color:#94a3b8;font-family:'Inter';">{feat['name']}</span>
                <div style="width:120px;height:8px;background:rgba(30,41,59,0.8);border-radius:4px;overflow:hidden;">
                    <div style="width:{bar_width}%;height:100%;background:{color};border-radius:4px;transition:width 0.3s;"></div>
                </div>
                <span style="font-family:'JetBrains Mono';font-size:0.75rem;color:{color};width:45px;text-align:right;">
                    {sign}{feat['impact']*100:.0f}%
                </span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")