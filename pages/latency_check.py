"""Latency Check page — Real-time API latency monitoring."""

import streamlit as st
import requests
import time
from datetime import datetime
import pandas as pd


ENDPOINTS = [
    {"url": "https://api.coingecko.com/api/v3/ping", "label": "CoinGecko API"},
    {"url": "https://s3.tradingview.com/tv.js", "label": "TradingView CDN"},
    {"url": "https://dns.google/resolve?name=api.coingecko.com&type=A", "label": "DNS Resolution"},
]


def measure_latency(url: str) -> dict:
    """Measure latency for a given URL."""
    try:
        start = time.perf_counter()
        resp = requests.get(url, timeout=10)
        latency_ms = round((time.perf_counter() - start) * 1000)
        return {
            "latency": latency_ms,
            "status": "success",
            "status_code": resp.status_code,
        }
    except requests.Timeout:
        return {"latency": None, "status": "timeout", "status_code": None}
    except Exception:
        return {"latency": None, "status": "error", "status_code": None}


def get_status_label(latency) -> tuple:
    """Return (label, color, icon) based on latency."""
    if latency is None:
        return ("Timeout", "#ef4444", "🔴")
    if latency < 200:
        return ("Excellent", "#22c55e", "🟢")
    if latency < 500:
        return ("Good", "#eab308", "🟡")
    return ("Slow", "#ef4444", "🔴")


def render():
    st.markdown('<h1 class="main-header">Latency Check</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time API latency monitoring — measures response times for all data sources.</p>', unsafe_allow_html=True)
    st.divider()

    # Initialize session state for history
    if "latency_history" not in st.session_state:
        st.session_state.latency_history = []

    col1, col2 = st.columns([1, 3])
    with col1:
        run_test = st.button("⚡ Run Latency Test", type="primary", use_container_width=True)

    if run_test:
        results = []
        progress = st.progress(0)

        for i, endpoint in enumerate(ENDPOINTS):
            result = measure_latency(endpoint["url"])
            result["label"] = endpoint["label"]
            result["timestamp"] = datetime.now().strftime("%H:%M:%S")
            results.append(result)
            progress.progress((i + 1) / len(ENDPOINTS))

        progress.empty()

        # Store in session state
        st.session_state.latest_results = results
        st.session_state.latency_history.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "CoinGecko": results[0]["latency"],
            "TradingView": results[1]["latency"],
            "DNS": results[2]["latency"],
        })

        # Keep only last 20 entries
        st.session_state.latency_history = st.session_state.latency_history[-20:]

    # Display results
    if "latest_results" in st.session_state:
        results = st.session_state.latest_results

        st.markdown('<h3 style="font-family:\'Sora\';color:#f1f5f9;margin:1.5rem 0 1rem;">📊 Latest Results</h3>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, result in enumerate(results):
            with cols[i]:
                label, color, indicator = get_status_label(result["latency"])
                latency_display = f"{result['latency']}ms" if result["latency"] else "N/A"

                st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <div class="metric-label">{result['label']}</div>
                    <div class="metric-value cyan" style="color:{color};">{latency_display}</div>
                    <div style="margin-top:0.5rem;font-size:0.85rem;color:#94a3b8;">{indicator} {label}</div>
                    <div style="margin-top:0.25rem;font-size:0.7rem;color:#475569;">
                        Checked: {result['timestamp']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Average
        valid_latencies = [r["latency"] for r in results if r["latency"] is not None]
        if valid_latencies:
            avg = round(sum(valid_latencies) / len(valid_latencies))
            st.markdown(f"""
            <div style="margin-top:1rem;padding:0.75rem 1.25rem;background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.15);border-radius:10px;">
                <span style="font-family:'Inter';font-size:0.9rem;color:#00d4ff;">⚡ Average latency: <strong>{avg}ms</strong> across {len(valid_latencies)} endpoints</span>
            </div>
            """, unsafe_allow_html=True)

    # History table
    if st.session_state.latency_history:
        st.divider()
        st.markdown('<h3 style="font-family:\'Sora\';color:#f1f5f9;margin-bottom:1rem;">📈 Latency History</h3>', unsafe_allow_html=True)

        df = pd.DataFrame(st.session_state.latency_history)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Chart
        if len(st.session_state.latency_history) > 1:
            import altair as alt

            chart_data = []
            for entry in st.session_state.latency_history:
                for key in ["CoinGecko", "TradingView", "DNS"]:
                    if entry[key] is not None:
                        chart_data.append({
                            "Time": entry["time"],
                            "Latency (ms)": entry[key],
                            "Endpoint": key,
                        })

            if chart_data:
                df_chart = pd.DataFrame(chart_data)
                chart = (
                    alt.Chart(df_chart)
                    .mark_line(point=True, strokeWidth=2)
                    .encode(
                        x=alt.X("Time:N", title="Time"),
                        y=alt.Y("Latency (ms):Q", title="Latency (ms)"),
                        color=alt.Color("Endpoint:N"),
                        tooltip=["Endpoint", "Time", "Latency (ms)"],
                    )
                    .properties(height=300)
                )
                st.altair_chart(chart, use_container_width=True)

    st.divider()

    # Performance thresholds info
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="glass-card">
            <div class="metric-label">Performance Thresholds</div>
            <div style="font-size:0.85rem;margin-top:0.75rem;color:#e2e8f0;line-height:2;">
                🟢 <strong>Excellent:</strong> &lt; 200ms<br>
                🟡 <strong>Good:</strong> 200-500ms<br>
                🔴 <strong>Slow:</strong> &gt; 500ms
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">Connection Info</div>
            <div style="font-size:0.85rem;margin-top:0.75rem;color:#e2e8f0;line-height:2;">
                📡 <strong>Endpoints:</strong> {len(ENDPOINTS)}<br>
                📊 <strong>History:</strong> {len(st.session_state.latency_history)} checks<br>
                🔄 <strong>Mode:</strong> Manual trigger
            </div>
        </div>
        """, unsafe_allow_html=True)