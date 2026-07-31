"""
BlockTrend-AI — The AI-first crypto intelligence platform
Deploy: streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="BlockTrend-AI | AI-First Crypto Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Premium dark UI CSS inspired by CryptoVision AI design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Sora:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* Global dark theme */
    .stApp {
        background: radial-gradient(ellipse at 50% 0%, #0d1b3e 0%, #070b1a 50%, #040711 100%);
        color: #e2e8f0;
    }

    /* Hide default streamlit elements for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar styling */
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1128 0%, #060d1f 100%);
        border-right: 1px solid rgba(0, 212, 255, 0.08);
    }

    div[data-testid="stSidebar"] .stRadio label {
        color: #94a3b8 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        padding: 0.5rem 0;
        transition: color 0.2s;
    }

    div[data-testid="stSidebar"] .stRadio label:hover {
        color: #00d4ff !important;
    }

    /* Main header - gradient text */
    .main-header {
        font-family: 'Sora', sans-serif;
        background: linear-gradient(135deg, #ffffff 0%, #00d4ff 50%, #0ea5e9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        line-height: 1.1;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        font-family: 'Inter', sans-serif;
        color: #64748b;
        font-size: 1.05rem;
        font-weight: 400;
        line-height: 1.6;
        max-width: 600px;
    }

    /* Hero section */
    .hero-container {
        text-align: center;
        padding: 4rem 2rem;
        max-width: 900px;
        margin: 0 auto;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(0, 212, 255, 0.08);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 9999px;
        padding: 0.4rem 1.2rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        font-weight: 500;
        color: #00d4ff;
        margin-bottom: 2rem;
    }

    .hero-badge::before {
        content: '';
        width: 8px;
        height: 8px;
        background: #00d4ff;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    .hero-title {
        font-family: 'Sora', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.15;
        letter-spacing: -0.03em;
        margin-bottom: 1.5rem;
    }

    .hero-title .cyan {
        background: linear-gradient(135deg, #00d4ff, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: #94a3b8;
        line-height: 1.7;
        max-width: 700px;
        margin: 0 auto 2.5rem;
    }

    .hero-buttons {
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
    }

    .btn-primary {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #0ea5e9, #0284c7);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0.8rem 2rem;
        border-radius: 12px;
        text-decoration: none;
        transition: all 0.3s;
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.3);
    }

    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(14, 165, 233, 0.4);
    }

    .btn-secondary {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0.8rem 2rem;
        border-radius: 12px;
        text-decoration: none;
        transition: all 0.3s;
    }

    .btn-secondary:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(0, 212, 255, 0.3);
    }

    .hero-note {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: #475569;
        margin-top: 1.5rem;
    }

    /* Glass cards */
    .glass-card {
        background: rgba(15, 23, 55, 0.6);
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s;
    }

    .glass-card:hover {
        border-color: rgba(0, 212, 255, 0.15);
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.05);
    }

    /* Metric cards */
    .metric-card {
        background: rgba(15, 23, 55, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #64748b;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: #f1f5f9;
    }

    /* Color classes */
    .bull { color: #22c55e; }
    .bear { color: #ef4444; }
    .cyan { color: #00d4ff; }

    /* Signal badges */
    .signal-badge {
        display: inline-block;
        padding: 0.3rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }

    .signal-buy {
        background: rgba(34, 197, 94, 0.12);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.25);
    }

    .signal-sell {
        background: rgba(239, 68, 68, 0.12);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.25);
    }

    .signal-hold {
        background: rgba(107, 114, 128, 0.12);
        color: #9ca3af;
        border: 1px solid rgba(107, 114, 128, 0.25);
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(15, 23, 55, 0.5);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        color: #94a3b8;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(0, 212, 255, 0.08) !important;
        border-color: rgba(0, 212, 255, 0.25) !important;
        color: #00d4ff !important;
    }

    /* Feature cards grid */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .feature-card {
        background: rgba(15, 23, 55, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s;
    }

    .feature-card:hover {
        border-color: rgba(0, 212, 255, 0.2);
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 212, 255, 0.08);
    }

    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }

    .feature-title {
        font-family: 'Sora', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 0.5rem;
    }

    .feature-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #64748b;
        line-height: 1.6;
    }

    /* Nav header */
    .nav-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }

    .nav-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'Sora', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
    }

    .nav-brand .icon {
        background: linear-gradient(135deg, #0ea5e9, #06b6d4);
        border-radius: 10px;
        padding: 6px 8px;
        font-size: 1rem;
    }

    .nav-brand .text {
        color: #f1f5f9;
    }

    .nav-brand .ai {
        color: #00d4ff;
    }

    /* Divider override */
    hr {
        border-color: rgba(255, 255, 255, 0.06) !important;
    }

    /* Button overrides */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }

    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.3) !important;
    }

    /* Dataframe styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Input styling */
    .stTextInput input, .stSelectbox select {
        background: rgba(15, 23, 55, 0.8) !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
        color: #e2e8f0 !important;
        border-radius: 10px !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #070b1a; }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #334155; }
</style>
""", unsafe_allow_html=True)

# Authentication
from auth import render_auth_ui, is_authenticated, render_user_sidebar

# Check if user is authenticated
if not is_authenticated():
    render_auth_ui()
else:
    # Sidebar navigation
    st.sidebar.markdown("""
    <div style="padding: 0.5rem 0 1.5rem;">
        <div class="nav-brand">
            <span class="icon">⚡</span>
            <span><span class="text">BlockTrend-</span><span class="ai">AI</span></span>
        </div>
        <div style="font-size:0.75rem;color:#475569;margin-top:0.25rem;padding-left:2.8rem;">AI-First Crypto Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

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