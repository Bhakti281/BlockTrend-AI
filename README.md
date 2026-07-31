# ⚡ BlockTrend-AI

**AI-Powered Crypto Intelligence Platform**

A professional Streamlit web application for cryptocurrency market analysis with ML ensemble predictions, TradingView chart integration, and real-time latency monitoring.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Features

- **📊 Market Dashboard** — Live crypto prices from CoinGecko with auto-refresh
- **📈 TradingView Charts** — Professional-grade candlestick charts with RSI, MACD, Bollinger Bands
- **🤖 AI Signals** — ML ensemble predictions (Random Forest, XGBoost, LSTM) with SHAP explanations
- **🪙 Multi-Coin Analysis** — Side-by-side comparison of BTC, ETH, SOL, ADA, BNB, XRP
- **⚡ Latency Monitor** — Real-time API response time tracking with history charts

## 🛠️ Tech Stack

- **Frontend**: Streamlit + Custom CSS (Dark Fintech Theme)
- **Data**: CoinGecko API (live prices), TradingView (charts)
- **ML**: Random Forest, XGBoost, LSTM ensemble (simulated predictions)
- **Visualization**: Altair charts, TradingView widget embeds
- **Typography**: Inter, Sora, JetBrains Mono

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Bhakti281/BlockTrend-AI.git
cd BlockTrend-AI

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 🌐 Deploy on Streamlit Cloud

1. Push this code to your GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository: `Bhakti281/BlockTrend-AI`
5. Set main file path: `app.py`
6. Click "Deploy"

That's it! Your app will be live at `https://blocktrend-ai.streamlit.app` (or similar).

## 📁 Project Structure

```
BlockTrend-AI/
├── app.py                    # Main Streamlit entry point
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .streamlit/
│   └── config.toml           # Streamlit theme & server config
└── pages/
    ├── __init__.py
    ├── dashboard.py          # Market Command Center
    ├── tradingview.py        # TradingView Charts integration
    ├── ai_signals.py         # ML ensemble predictions
    ├── multi_coin.py         # Multi-coin comparison
    └── latency_check.py      # API latency monitoring
```

## 🎨 Design

- **Theme**: Deep Midnight (#0a0e1f) + Electric Cyan (#00d4ff)
- **Style**: Glassmorphism cards, gradient accents, monospace data
- **Fonts**: Inter (body), Sora (headings), JetBrains Mono (data)

## ⚠️ Disclaimer

BlockTrend-AI is a **research and analytics tool only**. It does not provide financial advice or execute trades. AI predictions are for informational purposes. Always do your own research (DYOR).

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

Built with ⚡ by BlockTrend-AI