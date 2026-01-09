import aiohttp
from datetime import datetime
import config
from core.i18n import t

# =========================
# CONFIG
# =========================
MIN_VOLUME_USD = 10_000_000
VOLATILITY_THRESHOLD = 15.0
TOP_COINS_LIMIT = 50


async def fetch_market_data():
    url = f"{config.BINANCE_FUTURES_API}/fapi/v1/ticker/24hr"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception("Binance API error")
            return await response.json()


def format_volume(volume: float) -> str:
    if volume >= 1_000_000_000:
        return f"${volume / 1_000_000_000:.1f}B"
    return f"${volume / 1_000_000:.1f}M"


async def get_top_50_coins():
    data = await fetch_market_data()

    usdt_pairs = [
        tkr for tkr in data
        if tkr["symbol"].endswith("USDT")
        and tkr["symbol"] != "USDCUSDT"
    ]

    return sorted(
        usdt_pairs,
        key=lambda x: float(x.get("quoteVolume", 0)),
        reverse=True
    )[:TOP_COINS_LIMIT]


# =========================
# MAIN SUMMARY
# =========================
async def get_volatility_summary(user_id: int):
    top_coins = await get_top_50_coins()

    anomalies = []
    for tkr in top_coins:
        volume = float(tkr["quoteVolume"])
        price_change = abs(float(tkr["priceChangePercent"]))

        if volume >= MIN_VOLUME_USD and price_change >= VOLATILITY_THRESHOLD:
            anomalies.append({
                "symbol": tkr["symbol"].replace("USDT", ""),
                "price_change": float(tkr["priceChangePercent"]),
                "volume": volume,
            })

    anomalies.sort(key=lambda x: abs(x["price_change"]), reverse=True)

    message = (
        f"{t(user_id, 'volatility_header')}\n\n"
        f"{t(user_id, 'volatility_period')}\n"
        f"{t(user_id, 'volatility_filter')}\n\n"
    )

    if not anomalies:
        message += (
            f"{t(user_id, 'volatility_calm')}\n\n"
            f"{t(user_id, 'volatility_no_anomalies')}\n"
            f"{t(user_id, 'volatility_top50_ok')}\n"
            f"{t(user_id, 'volatility_analyzed_50')}\n"
        )
    else:
        message += f"{t(user_id, 'volatility_found')} <b>{len(anomalies)}</b>\n\n"

        for i, coin in enumerate(anomalies[:5], 1):
            emoji = "🟢" if coin["price_change"] > 0 else "🔴"
            message += (
                f"{i}. <b>{coin['symbol']}</b> {emoji}\n"
                f"   └ {coin['price_change']:+.1f}% | "
                f"{format_volume(coin['volume'])}\n"
            )

        pumps = sum(1 for c in anomalies if c["price_change"] > 0)
        dumps = len(anomalies) - pumps

        message += f"\n{t(user_id, 'volatility_context')}\n"

        if len(anomalies) >= 3:
            if pumps > dumps * 2:
                message += t(user_id, "volatility_mass_pump")
            elif dumps > pumps * 2:
                message += t(user_id, "volatility_mass_dump")
            else:
                message += t(user_id, "volatility_rotation")
        elif len(anomalies) == 2:
            message += t(user_id, "volatility_local")
        elif len(anomalies) == 1:
            message += (
                t(user_id, "volatility_single_pump")
                if pumps > 0
                else t(user_id, "volatility_single_dump")
            )

        total_volume = sum(c["volume"] for c in anomalies)
        message += f"\n{t(user_id, 'volatility_total_volume')} {format_volume(total_volume)}"

    message += f"\n\n⏱ {t(user_id, 'updated_at')} {datetime.now().strftime('%H:%M:%S')}"
    return message


# =========================
# ALERT CHECK
# =========================
async def check_volatility_for_alert():
    top_coins = await get_top_50_coins()

    anomalies = []
    for tkr in top_coins:
        volume = float(tkr["quoteVolume"])
        price_change = abs(float(tkr["priceChangePercent"]))

        if volume >= MIN_VOLUME_USD and price_change >= VOLATILITY_THRESHOLD:
            anomalies.append({
                "symbol": tkr["symbol"].replace("USDT", ""),
                "price_change": float(tkr["priceChangePercent"])
            })

    if len(anomalies) >= 5:
        pumps = sum(1 for c in anomalies if c["price_change"] > 0)
        dumps = len(anomalies) - pumps

        return {
            "count": len(anomalies),
            "pumps": pumps,
            "dumps": dumps,
            "top_coins": anomalies[:5],
        }

    return None
