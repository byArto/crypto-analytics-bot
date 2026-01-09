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


def format_volume(volume: float) -> str:
    if volume >= 1_000_000_000:
        return f"${volume / 1_000_000_000:.2f}B"
    return f"${volume / 1_000_000:.0f}M"


async def get_capital_flow_summary(user_id: int):
    data = await fetch_market_data()

    usdt_pairs = [
        tkr for tkr in data
        if tkr["symbol"].endswith("USDT")
        and tkr["symbol"] != "USDCUSDT"
    ]

    btc = next((tkr for tkr in usdt_pairs if tkr["symbol"] == "BTCUSDT"), None)
    eth = next((tkr for tkr in usdt_pairs if tkr["symbol"] == "ETHUSDT"), None)

    if not btc:
        raise Exception("BTC data unavailable")

    btc_change = float(btc["priceChangePercent"])
    btc_volume = float(btc["quoteVolume"])

    eth_change = float(eth["priceChangePercent"]) if eth else 0
    eth_volume = float(eth["quoteVolume"]) if eth else 0

    alts = sorted(
        [tkr for tkr in usdt_pairs if tkr["symbol"] not in ("BTCUSDT", "ETHUSDT")],
        key=lambda x: float(x.get("quoteVolume", 0)),
        reverse=True
    )[:20]

    alt_changes = [float(tkr["priceChangePercent"]) for tkr in alts]
    avg_alt_change = sum(alt_changes) / len(alt_changes) if alt_changes else 0
    total_alt_volume = sum(float(tkr["quoteVolume"]) for tkr in alts)

    message = (
        f"{t(user_id, 'flow_header')}\n\n"
        f"{t(user_id, 'flow_period')}\n\n"
        f"{t(user_id, 'flow_dynamics')}\n"
        f"• <b>BTC:</b> {btc_change:+.2f}% | {format_volume(btc_volume)}\n"
        f"• <b>ETH:</b> {eth_change:+.2f}% | {format_volume(eth_volume)}\n"
        f"• <b>{t(user_id, 'flow_alts_avg')}:</b> {avg_alt_change:+.2f}%\n"
        f"• <b>{t(user_id, 'flow_alts_volume')}:</b> {format_volume(total_alt_volume)}\n\n"
        f"{t(user_id, 'flow_analysis')}\n"
    )

    flow_diff = avg_alt_change - btc_change

    if abs(flow_diff) < 2:
        if btc_change > 0:
            message += t(user_id, "flow_sync_growth")
        elif btc_change < -2:
            message += t(user_id, "flow_sync_drop")
        else:
            message += t(user_id, "flow_calm")
    elif flow_diff > 5:
        message += (
            f"{t(user_id, 'flow_into_alts')}\n"
            f"{t(user_id, 'flow_diff')} {flow_diff:.1f}%"
        )
    elif flow_diff < -5:
        message += (
            f"{t(user_id, 'flow_into_btc')}\n"
            f"{t(user_id, 'flow_diff')} {abs(flow_diff):.1f}%"
        )
    else:
        if flow_diff > 0:
            message += f"{t(user_id, 'flow_soft_alts')} (+{flow_diff:.1f}%)"
        else:
            message += f"{t(user_id, 'flow_soft_btc')} (+{abs(flow_diff):.1f}%)"

    top_gainers = sorted(
        alts,
        key=lambda x: float(x["priceChangePercent"]),
        reverse=True
    )[:3]

    message += f"\n\n{t(user_id, 'flow_top_gainers')}\n"
    for i, alt in enumerate(top_gainers, 1):
        symbol = alt["symbol"].replace("USDT", "")
        change = float(alt["priceChangePercent"])
        volume = float(alt["quoteVolume"])
        message += f"{i}. <b>{symbol}</b>: {change:+.1f}% | {format_volume(volume)}\n"

    message += f"\n{t(user_id, 'updated_at')} {datetime.now().strftime('%H:%M:%S')}"
    return message
