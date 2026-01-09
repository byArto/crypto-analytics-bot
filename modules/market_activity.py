import aiohttp
from datetime import datetime
from core.i18n import t


# =========================
# FUTURES: Market Activity
# =========================
async def fetch_futures_tickers():
    """Fetch 24h futures tickers from Binance"""
    url = "https://fapi.binance.com/fapi/v1/ticker/24hr"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception("Binance Futures API error")
            return await response.json()


# =========================
# MAIN SUMMARY
# =========================
async def get_market_activity_summary(user_id: int):
    """
    Futures market activity:
    - volumes
    - price movement
    - overall sentiment
    """

    futures_data = await fetch_futures_tickers()

    futures_usdt = [
        tkr for tkr in futures_data
        if tkr["symbol"].endswith("USDT")
        and tkr["symbol"] != "USDCUSDT"
    ]

    sorted_by_volume = sorted(
        futures_usdt,
        key=lambda x: float(x["quoteVolume"]),
        reverse=True
    )

    top_10 = sorted_by_volume[:10]

    positive = sum(1 for tkr in top_10 if float(tkr["priceChangePercent"]) > 0)
    negative = len(top_10) - positive

    # --- Market Sentiment ---
    if positive > negative * 1.3:
        sentiment = t(user_id, "market_activity_sentiment_risk_on")
    elif negative > positive * 1.3:
        sentiment = t(user_id, "market_activity_sentiment_sell_pressure")
    else:
        sentiment = t(user_id, "market_activity_sentiment_mixed")

    # --- MESSAGE ---
    message = (
        f"{t(user_id, 'market_activity_header')}\n"
        f"{t(user_id, 'market_activity_period')}\n\n"
    )

    message += f"{t(user_id, 'market_activity_top_volume')}\n"

    for i, tkr in enumerate(top_10[:5], 1):
        symbol = tkr["symbol"].replace("USDT", "")
        raw_volume = float(tkr["quoteVolume"])
        change = float(tkr["priceChangePercent"])
        emoji = "🟢" if change >= 0 else "🔴"

        if raw_volume >= 1_000_000_000:
            volume_str = f"${raw_volume / 1_000_000_000:.1f}B"
        else:
            volume_str = f"${raw_volume / 1_000_000:.1f}M"

        message += (
            f"{i}. <b>{symbol}</b> — "
            f"{volume_str} {emoji} {change:+.2f}%\n"
        )

    message += (
        f"\n{t(user_id, 'market_activity_context_title')}\n"
        f"• {sentiment}\n\n"
        f"{t(user_id, 'market_activity_note')}\n"
        f"{t(user_id, 'updated_at')} {datetime.now().strftime('%H:%M:%S')}"
    )

    return message


# =========================
# MARKET STATE HELPERS
# =========================
async def is_market_red():
    futures_data = await fetch_futures_tickers()

    usdt_pairs = [
        tkr for tkr in futures_data
        if tkr["symbol"].endswith("USDT")
        and tkr["symbol"] != "USDCUSDT"
    ]

    top_50 = sorted(
        usdt_pairs,
        key=lambda x: float(x["quoteVolume"]),
        reverse=True
    )[:50]

    negative = sum(
        1 for tkr in top_50
        if float(tkr["priceChangePercent"]) < 0
    )

    return negative / len(top_50) >= 0.7


async def is_market_green():
    futures_data = await fetch_futures_tickers()

    usdt_pairs = [
        tkr for tkr in futures_data
        if tkr["symbol"].endswith("USDT")
        and tkr["symbol"] != "USDCUSDT"
    ]

    top_50 = sorted(
        usdt_pairs,
        key=lambda x: float(x["quoteVolume"]),
        reverse=True
    )[:50]

    positive = sum(
        1 for tkr in top_50
        if float(tkr["priceChangePercent"]) > 0
    )

    return positive / len(top_50) >= 0.7
