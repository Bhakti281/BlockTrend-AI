"""TradingView Charts page — Professional-grade charts with TradingView widget."""

import streamlit as st
import streamlit.components.v1 as components


SYMBOLS = {
    "BTC/USDT": "BINANCE:BTCUSDT",
    "ETH/USDT": "BINANCE:ETHUSDT",
    "SOL/USDT": "BINANCE:SOLUSDT",
    "ADA/USDT": "BINANCE:ADAUSDT",
    "BNB/USDT": "BINANCE:BNBUSDT",
    "XRP/USDT": "BINANCE:XRPUSDT",
}

INTERVALS = {
    "1 minute": "1",
    "5 minutes": "5",
    "15 minutes": "15",
    "1 hour": "60",
    "4 hours": "240",
    "1 day": "D",
    "1 week": "W",
}


def get_tradingview_widget(symbol: str, interval: str) -> str:
    """Generate TradingView Advanced Chart widget HTML."""
    return f"""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container" style="height:600px;width:100%;">
        <div class="tradingview-widget-container__widget" style="height:calc(100% - 32px);width:100%;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
        {{
            "autosize": true,
            "symbol": "{symbol}",
            "interval": "{interval}",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "backgroundColor": "rgba(7, 11, 26, 1)",
            "gridColor": "rgba(42, 46, 78, 0.2)",
            "hide_side_toolbar": false,
            "allow_symbol_change": true,
            "calendar": false,
            "studies": ["RSI@tv-basicstudies", "MACD@tv-basicstudies", "BB@tv-basicstudies"],
            "support_host": "https://www.tradingview.com"
        }}
        </script>
    </div>
    <!-- TradingView Widget END -->
    """


def render():
    st.markdown('<h1 class="main-header">TradingView Charts</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Professional-grade charts with real-time data, technical indicators, and drawing tools.</p>', unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        selected_pair = st.selectbox("Symbol", list(SYMBOLS.keys()), index=0)
    with col2:
        selected_interval = st.selectbox("Interval", list(INTERVALS.keys()), index=3)

    symbol = SYMBOLS[selected_pair]
    interval = INTERVALS[selected_interval]

    # Render TradingView widget
    widget_html = get_tradingview_widget(symbol, interval)
    components.html(widget_html, height=620)

    st.markdown("<br>", unsafe_allow_html=True)

    # Info cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="glass-card">
            <div class="metric-label">Indicators Active</div>
            <div style="font-size:0.85rem;color:#e2e8f0;line-height:1.8;margin-top:0.5rem;">
                • RSI (14)<br>
                • MACD (12,26,9)<br>
                • Bollinger Bands (20,2)
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card">
            <div class="metric-label">Chart Settings</div>
            <div style="font-size:0.85rem;color:#e2e8f0;line-height:1.8;margin-top:0.5rem;">
                • Style: Candlestick<br>
                • Theme: Dark Terminal<br>
                • Drawing Tools: Enabled
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">Data Source</div>
            <div style="font-size:0.85rem;color:#e2e8f0;line-height:1.8;margin-top:0.5rem;">
                • Provider: TradingView<br>
                • Exchange: Binance<br>
                • Symbol: {symbol}
            </div>
        </div>
        """, unsafe_allow_html=True)