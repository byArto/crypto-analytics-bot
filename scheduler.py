import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot

from modules.summary import get_market_summary
from modules.market_activity import is_market_red, is_market_green
import config

logger = logging.getLogger(__name__)

# Храним последние состояния чтобы не спамить одинаковыми алертами
last_market_state = {
    "red": False,
    "green": False,
}


async def check_and_send_alerts(bot: Bot):
    global last_market_state

    if not config.ALERT_CHAT_ID:
        logger.warning("⚠️ ALERT_CHAT_ID не настроен")
        return

    if not config.ENABLE_AUTO_ALERTS:
        logger.info("ℹ️ Авто-алерты отключены")
        return

    logger.info(f"🔍 Проверяю рынок... ({datetime.now().strftime('%H:%M:%S')})")

    try:
        # 🔴 Красный рынок
        is_red = await is_market_red()
        if is_red and not last_market_state["red"]:
            await bot.send_message(
                chat_id=config.ALERT_CHAT_ID,
                text=(
                    "🔴 <b>АЛЕРТ: РЫНОК ПОД ДАВЛЕНИЕМ</b>\n\n"
                    "Преобладает снижение по рынку."
                ),
                parse_mode="HTML"
            )
            last_market_state["red"] = True
            last_market_state["green"] = False

        elif not is_red:
            last_market_state["red"] = False

        # 🟢 Зелёный рынок
        is_green = await is_market_green()
        if is_green and not last_market_state["green"]:
            await bot.send_message(
                chat_id=config.ALERT_CHAT_ID,
                text=(
                    "🟢 <b>АЛЕРТ: РЫНОК СИЛЫ</b>\n\n"
                    "Преобладает рост по рынку."
                ),
                parse_mode="HTML"
            )
            last_market_state["green"] = True
            last_market_state["red"] = False

        elif not is_green:
            last_market_state["green"] = False

    except Exception as e:
        logger.error(f"❌ Ошибка в авто-алертах: {e}")


async def send_daily_summary(bot: Bot, period: str):
    """
    Отправляет ежедневную сводку рынка
    period: 'morning' | 'evening'
    """
    if not config.ALERT_CHAT_ID:
        return

    header = (
        "☀️ <b>УТРЕННЯЯ СВОДКА РЫНКА</b>\n\n"
        if period == "morning"
        else "🌙 <b>ВЕЧЕРНЯЯ СВОДКА РЫНКА</b>\n\n"
    )

    try:
        summary = await get_market_summary(config.ALERT_CHAT_ID)
        await bot.send_message(
            chat_id=config.ALERT_CHAT_ID,
            text=header + summary,
            parse_mode="HTML"
        )
        logger.info(f"📊 Отправлена {period} summary")

    except Exception as e:
        logger.error(f"❌ Ошибка отправки summary ({period}): {e}")


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()

    # 🔁 Периодическая проверка рынка
    scheduler.add_job(
        check_and_send_alerts,
        "interval",
        minutes=config.ALERT_CHECK_INTERVAL,
        args=[bot],
        id="market_check",
        replace_existing=True
    )

    # ☀️ Утренняя сводка — 06:00 UTC
    scheduler.add_job(
        send_daily_summary,
        trigger="cron",
        hour=6,
        minute=0,
        args=[bot, "morning"],
        id="daily_summary_morning",
        replace_existing=True
    )

    # 🌙 Вечерняя сводка — 18:00 UTC
    scheduler.add_job(
        send_daily_summary,
        trigger="cron",
        hour=18,
        minute=0,
        args=[bot, "evening"],
        id="daily_summary_evening",
        replace_existing=True
    )

    logger.info(
        f"⏰ Планировщик активен: проверка каждые {config.ALERT_CHECK_INTERVAL} минут"
    )

    return scheduler
