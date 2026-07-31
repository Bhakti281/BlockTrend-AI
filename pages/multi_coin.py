"""Multi-Coin Analysis page — Side-by-side coin comparison."""

import streamlit as st
import requests
import pandas as pd


def fetch_market_data():
    """Fetch detailed market data from CoinGecko."""
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
    st.markdown('<h1 class="main-header">Multi-Coin Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Compare BTC, ETH, SOL, ADA, BNB, XRP side-by-side with key metrics and 7-day sparklines.</p>', unsafe_allow_html=True)
    st.divider()

    data = fetch_market_data()

    if data is None:
        st.error("⚠️ Unable to fetch market data. CoinGecko API may be rate-limited.")
        return

    # Summary table
    st.markdown('<h3 style="font-family:\'Sora\';color:#f1f5f9;margin-bottom:1rem;">📊 Market Overview</h3>', unsafe_allow_html=True)
    table_data = []
    for coin in data:
        change = coin["price_change_percentage_24h"]
        table_data.append({
            "Coin": f"{coin['symbol'].upper()} ({coin['name']})",
            "Price": format_usd(coin["current_price"]),
            "24h Change": f"{change:+.2f}%",
            "Market Cap": format_usd(coin["market_cap"]),
            "24h Volume": format_usd(coin["total_volume"]),
            "24h High": format_usd(coin["high_24h"]),
            "24h Low": format_usd(coin["low_24h"]),
        })

    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Individual coin cards
    st.markdown('<h3 style="font-family:\'Sora\';color:#f1f5f9;margin-bottom:1rem;">🪙 Detailed Coin Cards</h3>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, coin in enumerate(data):
        with cols[i % 3]:
            change = coin["price_change_percentage_24h"]
            change_class = "bull" if change >= 0 else "bear"
            arrow = "▲" if change >= 0 else "▼"

            st.markdown(f"""
            <div class="glass-card" style="margin-bottom:1.25rem;">
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:1rem;">
                    <img src="{coin['image']}" width="40" height="40" style="border-radius:50%;border:2px solid rgba(255,255,255,0.06);">
                    <div>
                        <div style="font-family:'Sora';font-weight:600;color:#f1f5f9;">{coin['name']}</div>
                        <div style="font-size:0.75rem;color:#64748b;">{coin['symbol'].upper()}</div>
                    </div>
                </div>
                <div style="font-family:'JetBrains Mono';font-size:1.4rem;font-weight:700;color:#f1f5f9;">
                    {format_usd(coin['current_price'])}
                </div>
                <div class="{change_class}" style="font-size:0.85rem;margin-top:0.25rem;">
                    {arrow} {change:+.2f}%
                </div>
                <div style="margin-top:1rem;display:grid;grid-template-columns:1fr 1fr;gap:10px;font-size:0.75rem;">
                    <div><span style="color:#64748b;">Market Cap</span><br><span style="font-family:'JetBrains Mono';color:#e2e8f0;">{format_usd(coin['market_cap'])}</span></div>
                    <div><span style="color:#64748b;">Volume</span><br><span style="font-family:'JetBrains Mono';color:#e2e8f0;">{format_usd(coin['total_volume'])}</span></div>
                    <div><span style="color:#64748b;">24h High</span><br><span class="bull" style="font-family:'JetBrains Mono';">{format_usd(coin['high_24h'])}</span></div>
                    <div><span style="color:#64748b;">24h Low</span><br><span class="bear" style="font-family:'JetBrains Mono';">{format_usd(coin['low_24h'])}</span></div>
                </div>
                <div style="margin-top:0.75rem;padding-top:0.75rem;border-top:1px solid rgba(255,255,255,0.06);display:flex;justify-content:space-between;font-size:0.75rem;">
                    <span style="color:#64748b;">ATH</span>
                    <span style="font-family:'JetBrains Mono';color:#94a3b8;">{format_usd(coin['ath'])} ({coin['ath_change_percentage']:.1f}%)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 7-day sparkline chart
    st.divider()
    st.markdown('<h3 style="font-family:\'Sora\';color:#f1f5f9;margin-bottom:1rem;">📈 7-Day Price Trends</h3>', unsafe_allow_html=True)

    selected_coins = st.multiselect(
        "Select coins to compare",
        [c["name"] for c in data],
        default=[data[0]["name"], data[1]["name"]] if len(data) >= 2 else [data[0]["name"]],
    )

    if selected_coins:
        import altair as alt

        chart_data = []
        for coin in data:
            if coin["name"] in selected_coins and coin.get("sparkline_in_7d"):
                prices = coin["sparkline_in_7d"]["price"]
                for j, price in enumerate(prices):
                    chart_data.append({
                        "Hour": j,
                        "Price (USD)": price,
                        "Coin": coin["symbol"].upper(),
                    })

        if chart_data:
            df_chart = pd.DataFrame(chart_data)
            chart = (
                alt.Chart(df_chart)
                .mark_line(strokeWidth=2)
                .encode(
                    x=alt.X("Hour:Q", title="Hours (7 days)"),
                    y=alt.Y("Price (USD):Q", title="Price (USD)"),
                    color=alt.Color("Coin:N", legend=alt.Legend(title="Coin")),
                    tooltip=["Coin", "Hour", "Price (USD)"],
                )
                .properties(height=350)
                .configure_view(strokeWidth=0)
            )
            st.altair_chart(chart, use_container_width=True)