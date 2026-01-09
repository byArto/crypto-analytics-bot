📊 Crypto Analytics Telegram Bot

Telegram bot for crypto market analytics.  
Provides **market context**, not trading signals.

🚀 Features
- Market summary
- Anomalous volatility detection
- Funding rate analysis
- Long / Short ratio
- Capital flow (BTC ↔ Altcoins)
- Fear & Greed sentiment
- Market events overview

⚠️ Disclaimer
This bot **does NOT provide trading signals**.  
All data is for analytical and educational purposes only.

 🛠 Tech Stack
- Python 3.10+
- aiogram
- aiohttp
- Binance Futures API
- CoinGlass API

 📦 Installation (local)
```bash
git clone https://github.com/byArto/crypto-analytics-bot.git
cd crypto-analytics-bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
