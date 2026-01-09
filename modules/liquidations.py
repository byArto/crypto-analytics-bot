import aiohttp
from datetime import datetime
import config

COINGLASS_LIQUIDATIONS_URL = "https://open-api.coinglass.com/public/v2/liquidation_total"


async def fetch_liquidations():
    headers = {
        "accept": "application/json",
        "coinglassSecret": config.COINGLASS_API_KEY
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(COINGLASS_LIQUIDATIONS_URL, headers=headers) as response:
            if response.status != 200:
                raise Exception("Ошибка Coinglass API")
            return await response.json()


async def get_liquidations_summary():
    data = await fetch_liquidations()

    item = data["data"][0]  # рынок целиком

    total = float(item["total"])
    long = float(item["long"])
    short = float(item["short"])

    long_pct = long / total * 100
    short_pct = 100 - long_pct

    # формат суммы
    if total >= 1_000_000_000:
        total_str = f"${total / 1_000_000_000:.2f}B"
    else:
        total_str = f"${total / 1_000_000:.1f}M"

    if long_pct > short_pct * 1.3:
        context = "Преобладают ликвидации лонгов"
    elif short_pct > long_pct * 1.3:
        context = "Преобладают ликвидации шортов"
    else:
        context = "Ликвидации распределены относительно равномерно"

    message = (
        "🔥 <b>ЛИКВИДАЦИИ РЫНКА (24ч)</b>\n\n"
        f"💥 <b>Всего:</b> {total_str}\n"
        f"📊 Long: <b>{long_pct:.1f}%</b> | Short: <b>{short_pct:.1f}%</b>\n\n"
        f"🧠 <b>Контекст:</b> {context}\n\n"
        "ℹ️ Источник: Coinglass (Futures)\n"
        f"⏱ Обновлено: {datetime.now().strftime('%H:%M:%S')}"
    )

    return message
