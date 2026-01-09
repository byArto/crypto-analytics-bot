import aiohttp
import config
from core.i18n import t

BINANCE_FUNDING_ENDPOINT = "/fapi/v1/premiumIndex"

TOP_SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT",
    "XRPUSDT", "ADAUSDT", "AVAXUSDT", "DOGEUSDT",
    "LINKUSDT", "TONUSDT"
]


async def get_funding_rate_brief(user_id: int):
    """
    Локализованный краткий статус Funding Rate для summary
    """
    url = config.BINANCE_FUTURES_API + BINANCE_FUNDING_ENDPOINT

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

    fundings = []

    for item in data:
        if item.get("symbol") in TOP_SYMBOLS:
            try:
                fundings.append(float(item["lastFundingRate"]))
            except (KeyError, ValueError):
                continue

    if not fundings:
        return (
            f"{t(user_id, 'funding_header')}\n"
            f"{t(user_id, 'funding_unavailable')}"
        )

    avg_funding = sum(fundings) / len(fundings)

    # Интерпретация
    if avg_funding > 0.0007:
        state = t(user_id, "funding_long_overheat_title")
        comment = t(user_id, "funding_long_overheat_desc")
    elif avg_funding < -0.0007:
        state = t(user_id, "funding_short_overheat_title")
        comment = t(user_id, "funding_short_overheat_desc")
    else:
        state = t(user_id, "funding_neutral_title")
        comment = t(user_id, "funding_neutral_desc")

    return (
        f"{t(user_id, 'funding_header')}\n"
        f"{state}\n"
        f"ℹ️ {comment}"
    )
