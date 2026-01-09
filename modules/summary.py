import aiohttp

from core.i18n import t
from modules.market_activity import is_market_red, is_market_green
from modules.volatility import check_volatility_for_alert
from modules.events import get_high_importance_events_for_alert
from modules.funding_rate import get_funding_rate_brief

COINGECKO_GLOBAL_API = "https://api.coingecko.com/api/v3/global"


async def get_global_market_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(COINGECKO_GLOBAL_API) as resp:
            data = await resp.json()

    market_cap = data["data"]["total_market_cap"]["usd"]
    btc_dominance = data["data"]["market_cap_percentage"]["btc"]

    return market_cap, btc_dominance


def format_trillions(value: float) -> str:
    if value >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f}T"
    return f"${value / 1_000_000_000:.1f}B"


async def get_market_summary(user_id: int):
    # 🌍 Global market
    total_cap, btc_dom = await get_global_market_data()

    # 🔴 / 🟢 Market state
    is_red = await is_market_red()
    is_green = await is_market_green()

    if is_red:
        market_state = t(user_id, "summary_market_red_title")
        market_comment = t(user_id, "summary_market_red_desc")
    elif is_green:
        market_state = t(user_id, "summary_market_green_title")
        market_comment = t(user_id, "summary_market_green_desc")
    else:
        market_state = t(user_id, "summary_market_neutral_title")
        market_comment = t(user_id, "summary_market_neutral_desc")

    # ⚡ Volatility
    volatility = await check_volatility_for_alert()
    if volatility:
        vol_text = (
            f"{t(user_id, 'summary_volatility_title')}\n"
            f"{t(user_id, 'summary_volatility_count')}: <b>{volatility['count']}</b>\n"
            f"🟢 {t(user_id, 'summary_growth')}: {volatility['pumps']} | "
            f"🔴 {t(user_id, 'summary_fall')}: {volatility['dumps']}"
        )
    else:
        vol_text = t(user_id, "summary_volatility_none")

    # 📰 Events
    events = await get_high_importance_events_for_alert()
    if events:
        titles = ", ".join(
    t(user_id, e["title_key"]) for e in events[:3]
)
        events_text = (
            f"{t(user_id, 'summary_events_title')}: {len(events)}\n"
            f"ℹ️ {titles}"
        )
    else:
        events_text = t(user_id, "summary_events_none")

    # 📉 Funding
    funding_text = await get_funding_rate_brief(user_id)

    message = (
        f"{t(user_id, 'summary_header')}\n\n"
        f"🌐 <b>{t(user_id, 'summary_total_cap')}:</b> {format_trillions(total_cap)}\n"
        f"🟠 <b>{t(user_id, 'summary_btc_dom')}:</b> {btc_dom:.1f}%\n\n"
        f"{market_state}\n"
        f"ℹ️ {market_comment}\n\n"
        f"{vol_text}\n\n"
        f"{events_text}\n\n"
        f"{funding_text}\n\n"
        f"{t(user_id, 'summary_footer')}"
    )

    return message
