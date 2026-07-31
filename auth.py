"""
BlockTrend-AI — Supabase Authentication Module
Premium dark UI with hero landing page for unauthenticated users.
"""

import streamlit as st
from supabase import create_client, Client

# Initialize Supabase client
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "https://wadwjmtrxojmbrxtdomk.supabase.co")
SUPABASE_KEY = st.secrets.get("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndhZHdqbXRyeG9qbWJyeHRkb21rIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NTQ1OTQ1NywiZXhwIjoyMTAxMDM1NDU3fQ.vd58yUpgRwygZ-eU-mgohJS5MfeoUYfuG3kG1dkp_N0")


def get_supabase_client() -> Client:
    """Get or create Supabase client."""
    if "supabase_client" not in st.session_state:
        st.session_state.supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return st.session_state.supabase_client


def signup(email: str, password: str, full_name: str = "") -> dict:
    """Sign up a new user with email and password."""
    try:
        client = get_supabase_client()
        response = client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "full_name": full_name,
                }
            }
        })
        if response.user:
            st.session_state.user = response.user
            st.session_state.session = response.session
            return {"success": True, "user": response.user}
        return {"success": False, "error": "Signup failed. Please try again."}
    except Exception as e:
        return {"success": False, "error": str(e)}


def login(email: str, password: str) -> dict:
    """Sign in with email and password."""
    try:
        client = get_supabase_client()
        response = client.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })
        if response.user:
            st.session_state.user = response.user
            st.session_state.session = response.session
            return {"success": True, "user": response.user}
        return {"success": False, "error": "Invalid credentials."}
    except Exception as e:
        return {"success": False, "error": str(e)}


def logout():
    """Sign out the current user."""
    try:
        client = get_supabase_client()
        client.auth.sign_out()
    except Exception:
        pass
    finally:
        st.session_state.pop("user", None)
        st.session_state.pop("session", None)


def get_current_user():
    """Get the currently authenticated user from session state."""
    return st.session_state.get("user", None)


def is_authenticated() -> bool:
    """Check if a user is currently logged in."""
    return "user" in st.session_state and st.session_state.user is not None


def render_auth_ui():
    """
    Render the premium hero landing page + authentication UI.
    Matches the CryptoVision AI design language.
    """
    if is_authenticated():
        return True

    # Hero section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">Now with LSTM + Explainable AI</div>
        <h1 class="hero-title">
            The AI-first crypto<br>
            <span class="cyan">intelligence</span><br>
            platform
        </h1>
        <p class="hero-subtitle">
            Predict market moves with Random Forest, XGBoost, and LSTM.
            Understand every call with SHAP explanations. All wrapped in a beautiful trading terminal.
        </p>
        <p class="hero-note">No credit card. Powered by ML + Supabase Auth.</p>
    </div>
    """, unsafe_allow_html=True)

    # Features grid
    st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">ML Ensemble Predictions</div>
            <div class="feature-desc">Random Forest, XGBoost, and LSTM models vote on every signal with confidence scores.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">TradingView Charts</div>
            <div class="feature-desc">Professional-grade candlestick charts with RSI, MACD, and Bollinger Bands built in.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Real-Time Latency</div>
            <div class="feature-desc">Monitor API response times across all data sources with live latency tracking.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">SHAP Explanations</div>
            <div class="feature-desc">Understand why each prediction was made with feature importance visualizations.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🪙</div>
            <div class="feature-title">Multi-Coin Analysis</div>
            <div class="feature-desc">Compare BTC, ETH, SOL, ADA, BNB, XRP side-by-side with 7-day sparklines.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔐</div>
            <div class="feature-title">Secure Authentication</div>
            <div class="feature-desc">Powered by Supabase Auth with email/password sign-up and session management.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Auth forms
    st.markdown('<h2 style="text-align:center;font-family:\'Sora\';color:#f1f5f9;margin-bottom:1rem;">Get Started</h2>', unsafe_allow_html=True)

    col_spacer1, col_form, col_spacer2 = st.columns([1, 2, 1])

    with col_form:
        tab_login, tab_signup = st.tabs(["🔑 Sign In", "✨ Create Account"])

        with tab_login:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="Your password")
                submitted = st.form_submit_button("Sign In", type="primary", use_container_width=True)

                if submitted:
                    if not email or not password:
                        st.error("Please fill in all fields.")
                    else:
                        result = login(email, password)
                        if result["success"]:
                            st.success("✅ Logged in successfully!")
                            st.rerun()
                        else:
                            st.error(f"❌ {result['error']}")

        with tab_signup:
            with st.form("signup_form"):
                full_name = st.text_input("Full Name", placeholder="John Doe")
                email = st.text_input("Email", placeholder="you@example.com", key="signup_email")
                password = st.text_input("Password", type="password", placeholder="Min 6 characters", key="signup_pass")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
                submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)

                if submitted:
                    if not email or not password:
                        st.error("Please fill in all fields.")
                    elif password != confirm_password:
                        st.error("Passwords do not match.")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        result = signup(email, password, full_name)
                        if result["success"]:
                            st.success("✅ Account created! Check your email for verification.")
                            st.rerun()
                        else:
                            st.error(f"❌ {result['error']}")

    return False


def render_user_sidebar():
    """Render user info and logout button in sidebar."""
    user = get_current_user()
    if user:
        st.sidebar.markdown(f"""
        <div style="padding:0.75rem 1rem;margin:0.25rem 0.75rem;background:rgba(15,23,55,0.6);border-radius:10px;border:1px solid rgba(255,255,255,0.06);">
            <div style="display:flex;align-items:center;gap:10px;">
                <div style="width:32px;height:32px;background:linear-gradient(135deg,#0ea5e9,#7c3aed);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:0.8rem;color:#fff;">
                    {user.email[0].upper()}
                </div>
                <div>
                    <div style="font-size:0.8rem;color:#e2e8f0;font-weight:500;font-family:'Inter',sans-serif;">{user.email}</div>
                    <div style="font-size:0.65rem;color:#475569;font-family:'Inter',sans-serif;">Free Plan</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.sidebar.button("🚪 Sign Out", use_container_width=True):
            logout()
            st.rerun()