"""
BlockTrend-AI — Streamlit Crypto Intelligence Platform
Deploy: streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="BlockTrend-AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for dark fintech theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@600;700;800&family=JetBrains+Mono:wght@500;600&display=swap');

    .stApp {
        background: linear-gradient(180deg, #0a0e1f 0%, #060812 100%);
    }

    .main-header {
        font-family: 'Sora', sans-serif;
        background: linear-gradient(135deg, #00d4ff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.01em;
    }

    .metric-card {
        background: rgba(15, 18, 45, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #6b7280;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem;
        font-weight: 600;
        color: #f1f5f9;
    }

    .bull { color: #22c55e; }
    .bear { color: #ef4444; }
    .cyan { color: #00d4ff; }

    .glass-card {
        background: rgba(15, 18, 45, 0.55);
        backdrop-filter: blur(20px) saturate(160%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
    }

    .signal-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }

    .signal-buy {
        background: rgba(34, 197, 94, 0.15);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }

    .signal-sell {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    .signal-hold {
        background: rgba(107, 114, 128, 0.15);
        color: #9ca3af;
        border: 1px solid rgba(107, 114, 128, 0.3);
    }

    div[data-testid="stSidebar"] {
        background: rgba(10, 12, 30, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(15, 18, 45, 0.5);
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        color: #9ca3af;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(0, 212, 255, 0.1) !important;
        border-color: rgba(0, 212, 255, 0.3) !important;
        color: #00d4ff !important;
    }
</style>
""", unsafe_allow_html=True)

# Authentication
from auth import render_auth_ui, is_authenticated, render_user_sidebar

# Check if user is authenticated
if not is_authenticated():
    render_auth_ui()
else:
    # Sidebar navigation (only shown when logged in)
    st.sidebar.markdown("## ⚡ BlockTrend-AI")
    st.sidebar.markdown("*AI-Powered Crypto Intelligence*")
    st.sidebar.divider()

    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Dashboard", "📈 TradingView Charts", "🤖 AI Signals", "🪙 Multi-Coin", "⚡ Latency Check"],
        label_visibility="collapsed",
    )

    # Show user info and logout in sidebar
    render_user_sidebar()

    if page == "🏠 Dashboard":
        from pages import dashboard
        dashboard.render()
    elif page == "📈 TradingView Charts":
        from pages import tradingview
        tradingview.render()
    elif page == "🤖 AI Signals":
        from pages import ai_signals
        ai_signals.render()
    elif page == "🪙 Multi-Coin":
        from pages import multi_coin
        multi_coin.render()
    elif page == "⚡ Latency Check":
        from pages import latency_check
        latency_check.render()