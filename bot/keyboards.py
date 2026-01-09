from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)

def get_keyboard_with_ref():
    if not config.BINGX_REF_LINK:
        return None

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Торговать на BingX",
                    url=config.BINGX_REF_LINK
                )
            ]
        ]
    )
def get_main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📌 Сводка рынка")],  # первая, отдельно
            [KeyboardButton(text="/market"), KeyboardButton(text="/volatility")],
            [KeyboardButton(text="/flow"), KeyboardButton(text="/sentiment")],
            [KeyboardButton(text="/ratio"), KeyboardButton(text="/funding")],
            [KeyboardButton(text="/events")],
        ],
        resize_keyboard=True
    )
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def language_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
                InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en"),
            ]
        ]
    )
