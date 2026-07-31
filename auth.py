"""
BlockTrend-AI — Supabase Authentication Module
Handles signup, login, logout, and session management.
"""

import streamlit as st
from supabase import create_client, Client

# Initialize Supabase client
# Set these in .streamlit/secrets.toml or environment variables
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "https://wadwjmtrxojmbrxtdomk.supabase.co")
SUPABASE_KEY = st.secrets.get("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndhZHdqbXRyeG9qbWJyeHRkb21rIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NTQ1OTQ1NywiZXhwIjoyMTAxMDM1NDU3fQ.vd58yUpgRwygZ-eU-mgohJS5MfeoUYfuG3kG1dkp_N0")


def get_supabase_client() -> Client:
    """Get or create Supabase client."""
    if "supabase_client" not in st.session_state:
        st.session_state.supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return st.session_state.supabase_client


def signup(email: str, password: str, full_name: str = "") -> dict:
    """
    Sign up a new user with email and password.
    The handle_new_user() trigger will auto-create their profile.
    """
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
    Render the authentication UI (login/signup forms).
    Returns True if user is authenticated, False otherwise.
    """
    if is_authenticated():
        return True

    st.markdown('<h1 class="main-header">BlockTrend-AI</h1>', unsafe_allow_html=True)
    st.markdown("Sign in to access the AI-powered crypto intelligence platform.")
    st.divider()

    tab_login, tab_signup = st.tabs(["🔑 Login", "✨ Sign Up"])

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
        st.sidebar.divider()
        st.sidebar.markdown(f"👤 **{user.email}**")
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()