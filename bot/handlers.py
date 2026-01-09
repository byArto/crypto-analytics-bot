from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from core.lang import set_lang
from core.i18n import t
from bot.keyboards import get_keyboard_with_ref, language_keyboard
import config

# Модули
from modules.market_activity import get_market_activity_summary, is_market_red, is_market_green
from modules.volatility import get_volatility_summary, check_volatility_for_alert
from modules.capital_flow import get_capital_flow_summary
from modules.fear_greed import get_fear_greed_summary
from modules.long_short_ratio import get_long_short_summary
from modules.funding_rate import get_funding_rate_brief
from modules.events import get_events_summary
from modules.summary import get_market_summary

router = Router()
message_counter = 0


# ========= START =========
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        t(message.from_user.id, "start"),
        parse_mode="HTML"
    )


# ========= HELP =========
@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        t(message.from_user.id, "help"),
        parse_mode="HTML"
    )


# ========= LANGUAGE =========
@router.message(Command("language"))
async def cmd_language(message: Message):
    await message.answer(
        t(message.from_user.id, "choose_language"),
        reply_markup=language_keyboard()
    )


@router.callback_query(lambda c: c.data.startswith("lang_"))
async def change_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    set_lang(callback.from_user.id, lang)

    await callback.answer("OK")

    # автоматически показываем start на новом языке
    await callback.message.answer(
        t(callback.from_user.id, "start"),
        parse_mode="HTML"
    )


# ========= CHAT ID =========
@router.message(Command("chatid"))
async def chat_id(message: Message):
    await message.answer(
        f"<b>CHAT ID:</b> <code>{message.chat.id}</code>",
        parse_mode="HTML"
    )


# ========= MARKET =========
@router.message(Command("market"))
async def cmd_market(message: Message):
    global message_counter
    message_counter += 1

    await message.answer(t(message.from_user.id, "loading_market"))

    try:
        summary = await get_market_activity_summary(message.from_user.id)
        keyboard = None

        if config.SHOW_REF_BUTTON and message_counter % config.REF_BUTTON_FREQUENCY == 0:
            keyboard = get_keyboard_with_ref()

        await message.answer(summary, parse_mode="HTML", reply_markup=keyboard)

    except Exception:
        await message.answer(t(message.from_user.id, "error_generic"))


# ========= VOLATILITY =========
@router.message(Command("volatility"))
async def cmd_volatility(message: Message):
    global message_counter
    message_counter += 1

    await message.answer(t(message.from_user.id, "loading_volatility"))

    try:
        summary = await get_volatility_summary(message.from_user.id)
        keyboard = None

        if config.SHOW_REF_BUTTON and message_counter % config.REF_BUTTON_FREQUENCY == 0:
            keyboard = get_keyboard_with_ref()

        await message.answer(summary, parse_mode="HTML", reply_markup=keyboard)

    except Exception:
        await message.answer(t(message.from_user.id, "error_generic"))


# ========= FLOW =========
@router.message(Command("flow"))
async def cmd_flow(message: Message):
    global message_counter
    message_counter += 1

    await message.answer(t(message.from_user.id, "loading_flow"))

    try:
        summary = await get_capital_flow_summary(message.from_user.id)
        await message.answer(summary, parse_mode="HTML")

    except Exception:
        await message.answer(t(message.from_user.id, "error_generic"))


# ========= SENTIMENT =========
@router.message(Command("sentiment"))
async def cmd_sentiment(message: Message):
    global message_counter
    message_counter += 1

    await message.answer(t(message.from_user.id, "loading_sentiment"))

    try:
        summary = await get_fear_greed_summary(message.from_user.id)
        await message.answer(summary, parse_mode="HTML")

    except Exception:
        await message.answer(t(message.from_user.id, "error_generic"))


# ========= RATIO =========
@router.message(Command("ratio"))
async def cmd_ratio(message: Message):
    global message_counter
    message_counter += 1

    await message.answer(t(message.from_user.id, "loading_ratio"))

    try:
        summary = await get_long_short_summary(message.from_user.id)
        await message.answer(summary, parse_mode="HTML")

    except Exception:
        await message.answer(t(message.from_user.id, "error_generic"))


# ========= FUNDING =========
@router.message(Command("funding"))
async def cmd_funding(message: Message):
    await message.answer(t(message.from_user.id, "loading_funding"))

    try:
        text = await get_funding_rate_brief(message.from_user.id)
        await message.answer(text, parse_mode="HTML")
    except Exception:
        await message.answer(t(message.from_user.id, "error_generic"))


# ========= EVENTS =========
@router.message(Command("events"))
async def cmd_events(message: Message):
    await message.answer(t(message.from_user.id, "loading_events"))

    try:
        text = await get_events_summary(message.from_user.id)
        await message.answer(text, parse_mode="HTML")

    except Exception:
        await message.answer(t(message.from_user.id, "error_generic"))


# ========= SUMMARY =========
@router.message(Command("summary"))
async def cmd_summary(message: Message):
    await message.answer(t(message.from_user.id, "loading_summary"))

    try:
        text = await get_market_summary(message.from_user.id)
        await message.answer(text, parse_mode="HTML")

    except Exception:
        await message.answer(t(message.from_user.id, "error_generic"))


def register_handlers(dp):
    dp.include_router(router)
