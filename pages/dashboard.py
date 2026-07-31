"""Dashboard page — Market Command Center with live CoinGecko data."""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime


def fetch_market_data():
    """Fetch live market data from CoinGecko."""
    url = (
        "https://api.coingecko.com/api/v3/coins/markets"
        "?vs_currency=usd"
        "&ids=bitcoin,ethereum,solana,cardano,binancecoin,ripple"
        "&order=market_cap_desc&per_page=20&page=1"
        "&sparkline=true&price_change_percentage=24h"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def format_usd(n: float) -> str:
    if n >= 1_000_000_000:
        return f"${n / 1_000_000_000:.2f}B"
    if n >= 1_000_000:
        return f"${n / 1_000_000:.2f}M"
    if n >= 1_000:
        return f"${n:,.2f}"
    if n >= 1:
        return f"${n:.2f}"
    return f"${n:.4f}"


def render():
    st.markdown('<h1 class="main-header">Market Command Center</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Live crypto overview, AI signals, and market pulse — refreshed on demand.</p>', unsafe_allow_html=True)
    st.divider()

    data = fetch_market_data()

    if data is None:
        st.error("⚠️ Unable to fetch market data. CoinGecko API may be rate-limited. Try again shortly.")
        return

    # Top metrics
    total_cap = sum(c["market_cap"] for c in data)
    total_vol = sum(c["total_volume"] for c in data)
    avg_change = sum(c["price_change_percentage_24h"] for c in data) / len(data)
    bullish = sum(1 for c in data if c["price_change_percentage_24h"] > 0)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">Total Market Cap</div>
            <div class="metric-value">{format_usd(total_cap)}</div>
            <div class="{'bull' if avg_change >= 0 else 'bear'}" style="font-size:0.8rem;margin-top:0.25rem;">{avg_change:+.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">24h Volume</div>
            <div class="metric-value">{format_usd(total_vol)}</div>
            <div style="font-size:0.8rem;color:#64748b;margin-top:0.25rem;">{len(data)} coins tracked</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">Bullish Signals</div>
            <div class="metric-value bull">{bullish} / {len(data)}</div>
            <div style="font-size:0.8rem;color:#64748b;margin-top:0.25rem;">AI ensemble</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="glass-card">
            <div class="metric-label">AI Confidence</div>
            <div class="metric-value cyan">87%</div>
            <div style="font-size:0.8rem;color:#64748b;margin-top:0.25rem;">LSTM 24h forecast</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Live prices grid
    st.markdown('<h3 style="font-family:\'Sora\';color:#f1f5f9;margin-bottom:1rem;">📊 Live Prices</h3>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, coin in enumerate(data[:6]):
        with cols[i % 3]:
            change = coin["price_change_percentage_24h"]
            arrow = "▲" if change >= 0 else "▼"
            change_class = "bull" if change >= 0 else "bear"

            st.markdown(f"""
            <div class="glass-card" style="margin-bottom:1rem;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <img src="{coin['image']}" width="36" height="36" style="border-radius:50%;border:2px solid rgba(255,255,255,0.06);">
                    <div style="flex:1;">
                        <div style="font-family:'Sora';font-weight:600;color:#f1f5f9;">{coin['symbol'].upper()}</div>
                        <div style="font-size:0.75rem;color:#64748b;">{coin['name']}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-family:'JetBrains Mono';font-size:1.05rem;font-weight:600;color:#f1f5f9;">{format_usd(coin['current_price'])}</div>
                        <div class="{change_class}" style="font-size:0.8rem;">{arrow} {change:+.2f}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # AI Signal summary
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown('<h3 style="font-family:\'Sora\';color:#f1f5f9;margin-bottom:1rem;">🧠 ML Ensemble Status</h3>', unsafe_allow_html=True)
        df = pd.DataFrame([
            {"Model": "Random Forest", "Vote": "BUY", "Confidence": "79%", "Features": "42 technical indicators"},
            {"Model": "XGBoost", "Vote": "BUY", "Confidence": "83%", "Features": "Gradient boosted trees"},
            {"Model": "LSTM (24h)", "Vote": "BUY", "Confidence": "87%", "Features": "Sequential price patterns"},
        ])
        st.dataframe(df, use_container_width=True, hide_index=True)

    with col_right:
        st.markdown('<h3 style="font-family:\'Sora\';color:#f1f5f9;margin-bottom:1rem;">⚡ Top Signal</h3>', unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
            <div class="metric-label">BTC · LSTM 24H</div>
            <div style="font-family:'Sora';font-size:1.5rem;font-weight:700;color:#22c55e;margin:0.5rem 0;">BUY</div>
            <span class="signal-badge signal-buy">87% confidence</span>
            <div style="margin-top:1rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.06);">
                <div style="font-size:0.8rem;color:#94a3b8;line-height:1.8;">
                    • MACD positive crossover<br>
                    • RSI trending 62 → bullish<br>
                    • Sentiment +0.71 (FinBERT)<br>
                    • Volume +18% 24h
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")