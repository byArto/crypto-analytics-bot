# core/lang.py

USER_LANG = {}  # user_id -> "ru" | "en"

DEFAULT_LANG = "ru"


def get_lang(user_id: int) -> str:
    return USER_LANG.get(user_id, DEFAULT_LANG)


def set_lang(user_id: int, lang: str):
    USER_LANG[user_id] = lang
