import aiohttp
from datetime import datetime
import config
from core.i18n import t


async def fetch_long_short_ratio(symbol: str):
    url = f"{config.BINANCE_FUTURES_API}/futures/data/globalLongShortAccountRatio"
    params = {"symbol": symbol, "period": "5m", "limit": 1}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise Exception("Binance API error")
            data = await response.json()
            return data[0] if data else None


async def get_top_coins_data():
    url = f"{config.BINANCE_FUTURES_API}/fapi/v1/ticker/24hr"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception("Binance API error")

            data = await response.json()
            usdt_pairs = [
                t for t in data
                if t["symbol"].endswith("USDT") and t["symbol"] != "USDCUSDT"
            ]

            top = sorted(
                usdt_pairs,
                key=lambda x: float(x.get("quoteVolume", 0)),
                reverse=True
            )[:10]

            return [c["symbol"] for c in top]


# =========================
# MAIN SUMMARY
# =========================
async def get_long_short_summary(user_id: int):
    symbols = await get_top_coins_data()
    ratios = []

    for symbol in symbols[:8]:
        try:
            data = await fetch_long_short_ratio(symbol)
            if not data:
                continue

            ratio = float(data["longShortRatio"])
            ratios.append({
                "symbol": symbol.replace("USDT", ""),
                "ratio": ratio,
                "long": float(data["longAccount"]) * 100,
                "short": float(data["shortAccount"]) * 100,
            })
        except Exception:
            continue

    if not ratios:
        raise Exception("No L/S data")

    message = (
        f"{t(user_id, 'ratio_header')}\n\n"
        f"{t(user_id, 'ratio_subheader')}\n\n"
    )

    for i, c in enumerate(ratios[:5], 1):
        r = c["ratio"]

        if r > 1.5:
            bias = t(user_id, "ratio_bias_long")
            emoji = "📈"
        elif r < 0.67:
            bias = t(user_id, "ratio_bias_short")
            emoji = "📉"
        else:
            bias = t(user_id, "ratio_bias_neutral")
            emoji = "⚖️"

        message += (
            f"{i}. <b>{c['symbol']}</b> {emoji}\n"
            f"   └ Ratio: <b>{r:.2f}</b> ({bias})\n"
            f"   └ Long: {c['long']:.1f}% | Short: {c['short']:.1f}%\n\n"
        )

    avg_ratio = sum(c["ratio"] for c in ratios) / len(ratios)

    message += f"{t(user_id, 'ratio_analysis_title')}\n"

    if avg_ratio > 1.3:
        message += t(user_id, "ratio_analysis_long")
    elif avg_ratio < 0.77:
        message += t(user_id, "ratio_analysis_short")
    else:
        message += t(user_id, "ratio_analysis_neutral")

    long_biased = sum(1 for c in ratios if c["ratio"] > 1.5)
    short_biased = sum(1 for c in ratios if c["ratio"] < 0.67)
    balanced = len(ratios) - long_biased - short_biased

    message += (
        f"\n\n📈 {t(user_id, 'ratio_long_count')}: {long_biased}\n"
        f"📉 {t(user_id, 'ratio_short_count')}: {short_biased}\n"
        f"⚖️ {t(user_id, 'ratio_neutral_count')}: {balanced}\n"
        f"\n⏱ {t(user_id, 'updated_at')} {datetime.now().strftime('%H:%M:%S')}"
    )

    return message
