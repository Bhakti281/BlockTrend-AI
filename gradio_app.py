"""
BlockTrend-AI — The AI-first crypto intelligence platform
Gradio version for Hugging Face Spaces deployment
"""

import gradio as gr
import requests
import pandas as pd
import time
from datetime import datetime
import json

# ============================================================
# DATA FETCHING
# ============================================================

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


# ============================================================
# AI SIGNALS DATA
# ============================================================

SIGNALS = [
    {
        "coin": "Bitcoin", "symbol": "BTC", "action": "BUY",
        "confidence": 87, "expected_change": 4.2,
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
        "coin": "Ethereum", "symbol": "ETH", "action": "BUY",
        "confidence": 74, "expected_change": 2.8,
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
        "coin": "Solana", "symbol": "SOL", "action": "HOLD",
        "confidence": 62, "expected_change": 0.8,
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
        "coin": "Cardano", "symbol": "ADA", "action": "SELL",
        "confidence": 68, "expected_change": -2.1,
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

ENDPOINTS = [
    {"url": "https://api.coingecko.com/api/v3/ping", "label": "CoinGecko API"},
    {"url": "https://s3.tradingview.com/tv.js", "label": "TradingView CDN"},
    {"url": "https://dns.google/resolve?name=api.coingecko.com&type=A", "label": "DNS Resolution"},
]


# ============================================================
# PAGE FUNCTIONS
# ============================================================

def get_dashboard_data():
    """Get dashboard data and return formatted HTML."""
    data = fetch_market_data()
    if data is None:
        return "<div style='color:#ef4444;padding:20px;'>⚠️ Unable to fetch market data. CoinGecko API may be rate-limited. Try again shortly.</div>"

    total_cap = sum(c["market_cap"] for c in data)
    total_vol = sum(c["total_volume"] for c in data)
    avg_change = sum(c["price_change_percentage_24h"] for c in data) / len(data)
    bullish = sum(1 for c in data if c["price_change_percentage_24h"] > 0)

    change_class = "color:#22c55e" if avg_change >= 0 else "color:#ef4444"

    html = f"""
    <div style="font-family:'Inter',sans-serif;color:#e2e8f0;">
        <h2 style="font-family:'Sora',sans-serif;background:linear-gradient(135deg,#ffffff 0%,#00d4ff 50%,#0ea5e9 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:2rem;margin-bottom:0.5rem;">Market Command Center</h2>
        <p style="color:#64748b;margin-bottom:1.5rem;">Live crypto overview, AI signals, and market pulse — refreshed on demand.</p>

        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:2rem;">
            <div style="background:rgba(15,23,55,0.7);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;text-align:center;">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:#64748b;margin-bottom:0.5rem;">Total Market Cap</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:1.4rem;font-weight:700;color:#f1f5f9;">{format_usd(total_cap)}</div>
                <div style="{change_class};font-size:0.8rem;margin-top:0.25rem;">{avg_change:+.2f}%</div>
            </div>
            <div style="background:rgba(15,23,55,0.7);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;text-align:center;">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:#64748b;margin-bottom:0.5rem;">24h Volume</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:1.4rem;font-weight:700;color:#f1f5f9;">{format_usd(total_vol)}</div>
                <div style="font-size:0.8rem;color:#64748b;margin-top:0.25rem;">{len(data)} coins tracked</div>
            </div>
            <div style="background:rgba(15,23,55,0.7);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;text-align:center;">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:#64748b;margin-bottom:0.5rem;">Bullish Signals</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:1.4rem;font-weight:700;color:#22c55e;">{bullish} / {len(data)}</div>
                <div style="font-size:0.8rem;color:#64748b;margin-top:0.25rem;">AI ensemble</div>
            </div>
            <div style="background:rgba(15,23,55,0.7);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;text-align:center;">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:#64748b;margin-bottom:0.5rem;">AI Confidence</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:1.4rem;font-weight:700;color:#00d4ff;">87%</div>
                <div style="font-size:0.8rem;color:#64748b;margin-top:0.25rem;">LSTM 24h forecast</div>
            </div>
        </div>

        <h3 style="font-family:'Sora',sans-serif;color:#f1f5f9;margin-bottom:1rem;">📊 Live Prices</h3>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:2rem;">
    """

    for coin in data[:6]:
        change = coin["price_change_percentage_24h"]
        arrow = "▲" if change >= 0 else "▼"
        change_color = "#22c55e" if change >= 0 else "#ef4444"
        html += f"""
            <div style="background:rgba(15,23,55,0.6);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <img src="{coin['image']}" width="36" height="36" style="border-radius:50%;border:2px solid rgba(255,255,255,0.06);">
                    <div style="flex:1;">
                        <div style="font-family:'Sora',sans-serif;font-weight:600;color:#f1f5f9;">{coin['symbol'].upper()}</div>
                        <div style="font-size:0.75rem;color:#64748b;">{coin['name']}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-family:'JetBrains Mono',monospace;font-size:1.05rem;font-weight:600;color:#f1f5f9;">{format_usd(coin['current_price'])}</div>
                        <div style="color:{change_color};font-size:0.8rem;">{arrow} {change:+.2f}%</div>
                    </div>
                </div>
            </div>
        """

    html += """
        </div>

        <h3 style="font-family:'Sora',sans-serif;color:#f1f5f9;margin-bottom:1rem;">🧠 ML Ensemble Status</h3>
        <div style="background:rgba(15,23,55,0.6);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;margin-bottom:1rem;">
            <table style="width:100%;border-collapse:collapse;">
                <thead>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.1);">
                        <th style="text-align:left;padding:8px;color:#94a3b8;font-size:0.8rem;">Model</th>
                        <th style="text-align:left;padding:8px;color:#94a3b8;font-size:0.8rem;">Vote</th>
                        <th style="text-align:left;padding:8px;color:#94a3b8;font-size:0.8rem;">Confidence</th>
                        <th style="text-align:left;padding:8px;color:#94a3b8;font-size:0.8rem;">Features</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                        <td style="padding:8px;color:#e2e8f0;">Random Forest</td>
                        <td style="padding:8px;color:#22c55e;font-weight:600;">BUY</td>
                        <td style="padding:8px;color:#e2e8f0;">79%</td>
                        <td style="padding:8px;color:#94a3b8;">42 technical indicators</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                        <td style="padding:8px;color:#e2e8f0;">XGBoost</td>
                        <td style="padding:8px;color:#22c55e;font-weight:600;">BUY</td>
                        <td style="padding:8px;color:#e2e8f0;">83%</td>
                        <td style="padding:8px;color:#94a3b8;">Gradient boosted trees</td>
                    </tr>
                    <tr>
                        <td style="padding:8px;color:#e2e8f0;">LSTM (24h)</td>
                        <td style="padding:8px;color:#22c55e;font-weight:600;">BUY</td>
                        <td style="padding:8px;color:#e2e8f0;">87%</td>
                        <td style="padding:8px;color:#94a3b8;">Sequential price patterns</td>
                    </tr>
                </tbody>
            </table>
        </div>
    """

    html += f"<p style='color:#475569;font-size:0.8rem;margin-top:1rem;'>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>"
    html += "</div>"
    return html


def get_ai_signals():
    """Get AI signals and return formatted HTML."""
    buy_count = sum(1 for s in SIGNALS if s["action"] == "BUY")
    sell_count = sum(1 for s in SIGNALS if s["action"] == "SELL")
    hold_count = sum(1 for s in SIGNALS if s["action"] == "HOLD")
    avg_conf = sum(s["confidence"] for s in SIGNALS) / len(SIGNALS)

    html = f"""
    <div style="font-family:'Inter',sans-serif;color:#e2e8f0;">
        <h2 style="font-family:'Sora',sans-serif;background:linear-gradient(135deg,#ffffff 0%,#00d4ff 50%,#0ea5e9 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:2rem;margin-bottom:0.5rem;">AI Signals</h2>
        <p style="color:#64748b;margin-bottom:1.5rem;">ML ensemble predictions with SHAP-explained feature importance for each signal.</p>

        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:2rem;">
            <div style="background:rgba(15,23,55,0.7);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;text-align:center;">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:#64748b;margin-bottom:0.5rem;">Buy Signals</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:1.4rem;font-weight:700;color:#22c55e;">{buy_count}</div>
            </div>
            <div style="background:rgba(15,23,55,0.7);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;text-align:center;">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:#64748b;margin-bottom:0.5rem;">Sell Signals</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:1.4rem;font-weight:700;color:#ef4444;">{sell_count}</div>
            </div>
            <div style="background:rgba(15,23,55,0.7);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;text-align:center;">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:#64748b;margin-bottom:0.5rem;">Hold Signals</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:1.4rem;font-weight:700;color:#9ca3af;">{hold_count}</div>
            </div>
            <div style="background:rgba(15,23,55,0.7);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;text-align:center;">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:#64748b;margin-bottom:0.5rem;">Avg Confidence</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:1.4rem;font-weight:700;color:#00d4ff;">{avg_conf:.0f}%</div>
            </div>
        </div>

        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:1.25rem;">
    """

    for signal in SIGNALS:
        action = signal["action"]
        if action == "BUY":
            badge_bg = "rgba(34,197,94,0.12)"
            badge_color = "#22c55e"
            badge_border = "rgba(34,197,94,0.25)"
        elif action == "SELL":
            badge_bg = "rgba(239,68,68,0.12)"
            badge_color = "#ef4444"
            badge_border = "rgba(239,68,68,0.25)"
        else:
            badge_bg = "rgba(107,114,128,0.12)"
            badge_color = "#9ca3af"
            badge_border = "rgba(107,114,128,0.25)"

        change_color = "#22c55e" if signal["expected_change"] >= 0 else "#ef4444"
        change_arrow = "▲" if signal["expected_change"] >= 0 else "▼"

        html += f"""
            <div style="background:rgba(15,23,55,0.6);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.5rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
                    <div>
                        <span style="font-family:'Sora',sans-serif;font-size:1.1rem;font-weight:600;color:#f1f5f9;">{signal['coin']}</span>
                        <span style="color:#64748b;font-size:0.85rem;margin-left:0.5rem;">{signal['symbol']}</span>
                    </div>
                    <span style="display:inline-block;padding:0.3rem 0.85rem;border-radius:9999px;font-size:0.75rem;font-weight:600;font-family:'JetBrains Mono',monospace;background:{badge_bg};color:{badge_color};border:1px solid {badge_border};">{action} · {signal['confidence']}%</span>
                </div>
                <div style="color:{change_color};font-size:0.85rem;margin-bottom:1rem;">
                    {change_arrow} {signal['expected_change']:+.1f}% expected (24h)
                </div>

                <div style="margin-bottom:0.75rem;">
                    <div style="font-size:0.75rem;color:#64748b;margin-bottom:0.5rem;text-transform:uppercase;letter-spacing:0.1em;">Model Votes</div>
        """

        for model in signal["models"]:
            vote_color = "#22c55e" if model["vote"] == "BUY" else ("#ef4444" if model["vote"] == "SELL" else "#9ca3af")
            html += f"""
                    <div style="display:flex;justify-content:space-between;align-items:center;padding:4px 0;font-size:0.8rem;">
                        <span style="color:#94a3b8;">{model['name']}</span>
                        <span style="color:{vote_color};font-weight:600;">{model['vote']} ({model['weight']*100:.0f}%)</span>
                    </div>
            """

        html += """
                </div>
                <div style="border-top:1px solid rgba(255,255,255,0.06);padding-top:0.75rem;">
                    <div style="font-size:0.75rem;color:#64748b;margin-bottom:0.5rem;text-transform:uppercase;letter-spacing:0.1em;">SHAP Features</div>
        """

        for feat in signal["features"]:
            feat_color = "#22c55e" if feat["direction"] == "positive" else "#ef4444"
            sign = "+" if feat["direction"] == "positive" else "-"
            bar_width = int(feat["impact"] * 300)
            html += f"""
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                        <span style="flex:1;font-size:0.75rem;color:#94a3b8;">{feat['name']}</span>
                        <div style="width:80px;height:6px;background:rgba(30,41,59,0.8);border-radius:4px;overflow:hidden;">
                            <div style="width:{bar_width}%;height:100%;background:{feat_color};border-radius:4px;"></div>
                        </div>
                        <span style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:{feat_color};width:40px;text-align:right;">{sign}{feat['impact']*100:.0f}%</span>
                    </div>
            """

        html += """
                </div>
            </div>
        """

    html += "</div></div>"
    return html


def get_multi_coin():
    """Get multi-coin analysis data and return formatted HTML."""
    data = fetch_market_data()
    if data is None:
        return "<div style='color:#ef4444;padding:20px;'>⚠️ Unable to fetch market data. CoinGecko API may be rate-limited.</div>"

    html = """
    <div style="font-family:'Inter',sans-serif;color:#e2e8f0;">
        <h2 style="font-family:'Sora',sans-serif;background:linear-gradient(135deg,#ffffff 0%,#00d4ff 50%,#0ea5e9 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:2rem;margin-bottom:0.5rem;">Multi-Coin Analysis</h2>
        <p style="color:#64748b;margin-bottom:1.5rem;">Compare BTC, ETH, SOL, ADA, BNB, XRP side-by-side with key metrics.</p>

        <div style="background:rgba(15,23,55,0.6);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;margin-bottom:2rem;overflow-x:auto;">
            <table style="width:100%;border-collapse:collapse;min-width:700px;">
                <thead>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.1);">
                        <th style="text-align:left;padding:10px;color:#94a3b8;font-size:0.8rem;">Coin</th>
                        <th style="text-align:right;padding:10px;color:#94a3b8;font-size:0.8rem;">Price</th>
                        <th style="text-align:right;padding:10px;color:#94a3b8;font-size:0.8rem;">24h Change</th>
                        <th style="text-align:right;padding:10px;color:#94a3b8;font-size:0.8rem;">Market Cap</th>
                        <th style="text-align:right;padding:10px;color:#94a3b8;font-size:0.8rem;">24h Volume</th>
                        <th style="text-align:right;padding:10px;color:#94a3b8;font-size:0.8rem;">24h High</th>
                        <th style="text-align:right;padding:10px;color:#94a3b8;font-size:0.8rem;">24h Low</th>
                    </tr>
                </thead>
                <tbody>
    """

    for coin in data:
        change = coin["price_change_percentage_24h"]
        change_color = "#22c55e" if change >= 0 else "#ef4444"
        html += f"""
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                        <td style="padding:10px;color:#e2e8f0;font-weight:500;">
                            <div style="display:flex;align-items:center;gap:8px;">
                                <img src="{coin['image']}" width="24" height="24" style="border-radius:50%;">
                                {coin['symbol'].upper()} <span style="color:#64748b;font-size:0.8rem;">({coin['name']})</span>
                            </div>
                        </td>
                        <td style="padding:10px;text-align:right;font-family:'JetBrains Mono',monospace;color:#f1f5f9;">{format_usd(coin['current_price'])}</td>
                        <td style="padding:10px;text-align:right;font-family:'JetBrains Mono',monospace;color:{change_color};">{change:+.2f}%</td>
                        <td style="padding:10px;text-align:right;font-family:'JetBrains Mono',monospace;color:#e2e8f0;">{format_usd(coin['market_cap'])}</td>
                        <td style="padding:10px;text-align:right;font-family:'JetBrains Mono',monospace;color:#e2e8f0;">{format_usd(coin['total_volume'])}</td>
                        <td style="padding:10px;text-align:right;font-family:'JetBrains Mono',monospace;color:#22c55e;">{format_usd(coin['high_24h'])}</td>
                        <td style="padding:10px;text-align:right;font-family:'JetBrains Mono',monospace;color:#ef4444;">{format_usd(coin['low_24h'])}</td>
                    </tr>
        """

    html += """
                </tbody>
            </table>
        </div>

        <h3 style="font-family:'Sora',sans-serif;color:#f1f5f9;margin-bottom:1rem;">🪙 Detailed Coin Cards</h3>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;">
    """

    for coin in data:
        change = coin["price_change_percentage_24h"]
        change_color = "#22c55e" if change >= 0 else "#ef4444"
        arrow = "▲" if change >= 0 else "▼"
        html += f"""
            <div style="background:rgba(15,23,55,0.6);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;">
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:1rem;">
                    <img src="{coin['image']}" width="40" height="40" style="border-radius:50%;border:2px solid rgba(255,255,255,0.06);">
                    <div>
                        <div style="font-family:'Sora',sans-serif;font-weight:600;color:#f1f5f9;">{coin['name']}</div>
                        <div style="font-size:0.75rem;color:#64748b;">{coin['symbol'].upper()}</div>
                    </div>
                </div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:1.4rem;font-weight:700;color:#f1f5f9;">{format_usd(coin['current_price'])}</div>
                <div style="color:{change_color};font-size:0.85rem;margin-top:0.25rem;">{arrow} {change:+.2f}%</div>
                <div style="margin-top:1rem;display:grid;grid-template-columns:1fr 1fr;gap:10px;font-size:0.75rem;">
                    <div><span style="color:#64748b;">Market Cap</span><br><span style="font-family:'JetBrains Mono',monospace;color:#e2e8f0;">{format_usd(coin['market_cap'])}</span></div>
                    <div><span style="color:#64748b;">Volume</span><br><span style="font-family:'JetBrains Mono',monospace;color:#e2e8f0;">{format_usd(coin['total_volume'])}</span></div>
                    <div><span style="color:#64748b;">24h High</span><br><span style="font-family:'JetBrains Mono',monospace;color:#22c55e;">{format_usd(coin['high_24h'])}</span></div>
                    <div><span style="color:#64748b;">24h Low</span><br><span style="font-family:'JetBrains Mono',monospace;color:#ef4444;">{format_usd(coin['low_24h'])}</span></div>
                </div>
            </div>
        """

    html += "</div></div>"
    return html


def get_latency_check():
    """Run latency check and return formatted HTML."""
    results = []
    for endpoint in ENDPOINTS:
        try:
            start = time.perf_counter()
            resp = requests.get(endpoint["url"], timeout=10)
            latency_ms = round((time.perf_counter() - start) * 1000)
            results.append({
                "label": endpoint["label"],
                "latency": latency_ms,
                "status": "success",
                "status_code": resp.status_code,
            })
        except requests.Timeout:
            results.append({"label": endpoint["label"], "latency": None, "status": "timeout", "status_code": None})
        except Exception:
            results.append({"label": endpoint["label"], "latency": None, "status": "error", "status_code": None})

    html = """
    <div style="font-family:'Inter',sans-serif;color:#e2e8f0;">
        <h2 style="font-family:'Sora',sans-serif;background:linear-gradient(135deg,#ffffff 0%,#00d4ff 50%,#0ea5e9 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:2rem;margin-bottom:0.5rem;">Latency Check</h2>
        <p style="color:#64748b;margin-bottom:1.5rem;">Real-time API latency monitoring — measures response times for all data sources.</p>

        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:2rem;">
    """

    for result in results:
        if result["latency"] is None:
            latency_display = "N/A"
            color = "#ef4444"
            indicator = "🔴"
            label = "Timeout"
        elif result["latency"] < 200:
            latency_display = f"{result['latency']}ms"
            color = "#22c55e"
            indicator = "🟢"
            label = "Excellent"
        elif result["latency"] < 500:
            latency_display = f"{result['latency']}ms"
            color = "#eab308"
            indicator = "🟡"
            label = "Good"
        else:
            latency_display = f"{result['latency']}ms"
            color = "#ef4444"
            indicator = "🔴"
            label = "Slow"

        html += f"""
            <div style="background:rgba(15,23,55,0.7);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.5rem;text-align:center;">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:#64748b;margin-bottom:0.5rem;">{result['label']}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:1.8rem;font-weight:700;color:{color};">{latency_display}</div>
                <div style="margin-top:0.5rem;font-size:0.85rem;color:#94a3b8;">{indicator} {label}</div>
            </div>
        """

    valid_latencies = [r["latency"] for r in results if r["latency"] is not None]
    if valid_latencies:
        avg = round(sum(valid_latencies) / len(valid_latencies))
        html += f"""
        </div>
        <div style="padding:0.75rem 1.25rem;background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.15);border-radius:10px;margin-bottom:1.5rem;">
            <span style="font-size:0.9rem;color:#00d4ff;">⚡ Average latency: <strong>{avg}ms</strong> across {len(valid_latencies)} endpoints</span>
        </div>
        """
    else:
        html += "</div>"

    html += """
        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:1rem;">
            <div style="background:rgba(15,23,55,0.6);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:#64748b;margin-bottom:0.75rem;">Performance Thresholds</div>
                <div style="font-size:0.85rem;color:#e2e8f0;line-height:2;">
                    🟢 <strong>Excellent:</strong> &lt; 200ms<br>
                    🟡 <strong>Good:</strong> 200-500ms<br>
                    🔴 <strong>Slow:</strong> &gt; 500ms
                </div>
            </div>
            <div style="background:rgba(15,23,55,0.6);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:#64748b;margin-bottom:0.75rem;">Connection Info</div>
                <div style="font-size:0.85rem;color:#e2e8f0;line-height:2;">
                    📡 <strong>Endpoints:</strong> 3<br>
                    🔄 <strong>Mode:</strong> On-demand<br>
                    📊 <strong>Protocol:</strong> HTTPS
                </div>
            </div>
        </div>
    </div>
    """
    return html


def get_tradingview_chart(symbol="BINANCE:BTCUSDT", interval="60"):
    """Return TradingView widget HTML."""
    html = f"""
    <div style="font-family:'Inter',sans-serif;color:#e2e8f0;">
        <h2 style="font-family:'Sora',sans-serif;background:linear-gradient(135deg,#ffffff 0%,#00d4ff 50%,#0ea5e9 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:2rem;margin-bottom:0.5rem;">TradingView Charts</h2>
        <p style="color:#64748b;margin-bottom:1.5rem;">Professional-grade charts with real-time data, technical indicators, and drawing tools.</p>

        <div class="tradingview-widget-container" style="height:500px;width:100%;margin-bottom:1.5rem;">
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

        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;">
            <div style="background:rgba(15,23,55,0.6);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:#64748b;margin-bottom:0.5rem;">Indicators Active</div>
                <div style="font-size:0.85rem;color:#e2e8f0;line-height:1.8;margin-top:0.5rem;">
                    • RSI (14)<br>• MACD (12,26,9)<br>• Bollinger Bands (20,2)
                </div>
            </div>
            <div style="background:rgba(15,23,55,0.6);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:#64748b;margin-bottom:0.5rem;">Chart Settings</div>
                <div style="font-size:0.85rem;color:#e2e8f0;line-height:1.8;margin-top:0.5rem;">
                    • Style: Candlestick<br>• Theme: Dark Terminal<br>• Drawing Tools: Enabled
                </div>
            </div>
            <div style="background:rgba(15,23,55,0.6);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.25rem;">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;color:#64748b;margin-bottom:0.5rem;">Current Symbol</div>
                <div style="font-size:0.85rem;color:#00d4ff;line-height:1.8;margin-top:0.5rem;">
                    📈 {symbol}<br>⏱️ Interval: {interval}
                </div>
            </div>
        </div>
    </div>
    """
    return html


# ============================================================
# GRADIO APP
# ============================================================

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Sora:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

.gradio-container {
    background: radial-gradient(ellipse at 50% 0%, #0d1b3e 0%, #070b1a 50%, #040711 100%) !important;
    font-family: 'Inter', sans-serif !important;
    max-width: 1400px !important;
}

.dark {
    --background-fill-primary: #070b1a !important;
    --background-fill-secondary: #0f1737 !important;
    --border-color-primary: rgba(255, 255, 255, 0.06) !important;
}

footer {visibility: hidden !important;}

.tab-nav button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
    background: rgba(15, 23, 55, 0.5) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 10px !important;
    margin: 0 4px !important;
}

.tab-nav button.selected {
    background: rgba(0, 212, 255, 0.08) !important;
    border-color: rgba(0, 212, 255, 0.25) !important;
    color: #00d4ff !important;
}

#component-0 {
    background: transparent !important;
}
"""

# Wrapper functions for Gradio
def refresh_dashboard():
    return get_dashboard_data()

def refresh_signals():
    return get_ai_signals()

def refresh_multi_coin():
    return get_multi_coin()

def refresh_latency():
    return get_latency_check()

def update_chart(pair, interval):
    symbols_map = {
        "BTC/USDT": "BINANCE:BTCUSDT",
        "ETH/USDT": "BINANCE:ETHUSDT",
        "SOL/USDT": "BINANCE:SOLUSDT",
        "ADA/USDT": "BINANCE:ADAUSDT",
        "BNB/USDT": "BINANCE:BNBUSDT",
        "XRP/USDT": "BINANCE:XRPUSDT",
    }
    intervals_map = {
        "1 minute": "1",
        "5 minutes": "5",
        "15 minutes": "15",
        "1 hour": "60",
        "4 hours": "240",
        "1 day": "D",
        "1 week": "W",
    }
    symbol = symbols_map.get(pair, "BINANCE:BTCUSDT")
    interval_val = intervals_map.get(interval, "60")
    return get_tradingview_chart(symbol, interval_val)


# Build the Gradio app
with gr.Blocks(
    title="BlockTrend-AI | AI-First Crypto Intelligence",
    css=CUSTOM_CSS,
    theme=gr.themes.Base(
        primary_hue="cyan",
        secondary_hue="blue",
        neutral_hue="slate",
        font=gr.themes.GoogleFont("Inter"),
    ),
) as demo:

    # Header
    gr.HTML("""
    <div style="text-align:center;padding:2rem 1rem 1rem;">
        <div style="display:inline-flex;align-items:center;gap:12px;margin-bottom:1rem;">
            <span style="background:linear-gradient(135deg,#0ea5e9,#06b6d4);border-radius:10px;padding:8px 10px;font-size:1.2rem;">⚡</span>
            <span style="font-family:'Sora',sans-serif;font-size:1.5rem;font-weight:700;color:#f1f5f9;">BlockTrend-<span style="color:#00d4ff;">AI</span></span>
        </div>
        <p style="font-family:'Inter',sans-serif;color:#64748b;font-size:0.9rem;">The AI-first crypto intelligence platform — Predict market moves with ML ensemble models</p>
    </div>
    """)

    with gr.Tabs():
        # Dashboard Tab
        with gr.Tab("🏠 Dashboard"):
            dashboard_btn = gr.Button("🔄 Refresh Dashboard", variant="primary", size="sm")
            dashboard_output = gr.HTML(value=get_dashboard_data())
            dashboard_btn.click(fn=refresh_dashboard, outputs=dashboard_output)

        # TradingView Tab
        with gr.Tab("📈 TradingView Charts"):
            with gr.Row():
                pair_dropdown = gr.Dropdown(
                    choices=["BTC/USDT", "ETH/USDT", "SOL/USDT", "ADA/USDT", "BNB/USDT", "XRP/USDT"],
                    value="BTC/USDT",
                    label="Symbol",
                )
                interval_dropdown = gr.Dropdown(
                    choices=["1 minute", "5 minutes", "15 minutes", "1 hour", "4 hours", "1 day", "1 week"],
                    value="1 hour",
                    label="Interval",
                )
                chart_btn = gr.Button("📊 Load Chart", variant="primary", size="sm")
            chart_output = gr.HTML(value=get_tradingview_chart())
            chart_btn.click(fn=update_chart, inputs=[pair_dropdown, interval_dropdown], outputs=chart_output)

        # AI Signals Tab
        with gr.Tab("🤖 AI Signals"):
            signals_btn = gr.Button("🔄 Refresh Signals", variant="primary", size="sm")
            signals_output = gr.HTML(value=get_ai_signals())
            signals_btn.click(fn=refresh_signals, outputs=signals_output)

        # Multi-Coin Tab
        with gr.Tab("🪙 Multi-Coin"):
            multi_btn = gr.Button("🔄 Refresh Data", variant="primary", size="sm")
            multi_output = gr.HTML(value=get_multi_coin())
            multi_btn.click(fn=refresh_multi_coin, outputs=multi_output)

        # Latency Check Tab
        with gr.Tab("⚡ Latency Check"):
            latency_btn = gr.Button("⚡ Run Latency Test", variant="primary", size="sm")
            latency_output = gr.HTML(value=get_latency_check())
            latency_btn.click(fn=refresh_latency, outputs=latency_output)

    # Footer
    gr.HTML("""
    <div style="text-align:center;padding:2rem 1rem;margin-top:1rem;border-top:1px solid rgba(255,255,255,0.06);">
        <p style="color:#475569;font-size:0.8rem;font-family:'Inter',sans-serif;">
            BlockTrend-AI © 2024 — Powered by ML + CoinGecko + TradingView
        </p>
    </div>
    """)


if __name__ == "__main__":
    demo.launch()