import aiohttp
from datetime import datetime
import config
from core.i18n import t


async def fetch_market_data():
    url = f"{config.BINANCE_FUTURES_API}/fapi/v1/ticker/24hr"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception("Binance API error")
            return await response.json()


def calculate_fear_greed_score(data: list):
    usdt_pairs = [
        x for x in data
        if x["symbol"].endswith("USDT") and x["symbol"] != "USDCUSDT"
    ]

    top_50 = sorted(
        usdt_pairs,
        key=lambda x: float(x.get("quoteVolume", 0)),
        reverse=True
    )[:50]

    positive = sum(1 for x in top_50 if float(x["priceChangePercent"]) > 0)
    negative = len(top_50) - positive
    positive_ratio = positive / len(top_50)

    sentiment_score = positive_ratio * 100 * 0.4

    avg_volatility = sum(
        abs(float(x["priceChangePercent"])) for x in top_50
    ) / len(top_50)

    if avg_volatility < 5:
        volatility_score = 50 * 0.3
    elif avg_volatility > 10:
        volatility_score = (80 if positive_ratio > 0.6 else 20) * 0.3
    else:
        volatility_score = 50 * 0.3

    total_volume = sum(float(x["quoteVolume"]) for x in top_50)
    avg_volume = total_volume / len(top_50)

    if avg_volume > 200_000_000:
        volume_score = 70 * 0.3
    elif avg_volume < 50_000_000:
        volume_score = 40 * 0.3
    else:
        volume_score = 50 * 0.3

    score = sentiment_score + volatility_score + volume_score

    return score, positive, negative, avg_volatility


async def get_fear_greed_summary(user_id: int):
    data = await fetch_market_data()
    score, positive, negative, avg_volatility = calculate_fear_greed_score(data)

    if score >= 75:
        level = t(user_id, "fg_extreme_greed")
        emoji = "🤑"
        desc = t(user_id, "fg_extreme_greed_desc")
    elif score >= 60:
        level = t(user_id, "fg_greed")
        emoji = "😄"
        desc = t(user_id, "fg_greed_desc")
    elif score >= 45:
        level = t(user_id, "fg_neutral")
        emoji = "😐"
        desc = t(user_id, "fg_neutral_desc")
    elif score >= 30:
        level = t(user_id, "fg_fear")
        emoji = "😰"
        desc = t(user_id, "fg_fear_desc")
    else:
        level = t(user_id, "fg_extreme_fear")
        emoji = "😱"
        desc = t(user_id, "fg_extreme_fear_desc")

    filled = int(score / 10)
    bar = "🟩" * filled + "⬜" * (10 - filled)

    message = (
        f"{emoji} <b>{t(user_id, 'fg_header')}</b>\n\n"
        f"📊 <b>{t(user_id, 'fg_score')}:</b> {int(score)}/100\n"
        f"🎯 <b>{t(user_id, 'fg_status')}:</b> {level}\n"
        f"💡 <i>{desc}</i>\n\n"
        f"{bar}\n\n"
        f"📈 <b>{t(user_id, 'fg_stats')}</b>\n"
        f"• {t(user_id, 'fg_positive')}: {positive}\n"
        f"• {t(user_id, 'fg_negative')}: {negative}\n"
        f"• {t(user_id, 'fg_volatility')}: {avg_volatility:.2f}%\n\n"
        f"⏱ {t(user_id, 'updated_at')} {datetime.now().strftime('%H:%M:%S')}"
    )

    return message
