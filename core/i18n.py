from i18n.ru import TEXTS as RU
from i18n.en import TEXTS as EN
from core.lang import get_lang

LANG_MAP = {
    "ru": RU,
    "en": EN,
}

def t(user_id: int, key: str) -> str:
    lang = get_lang(user_id)
    return LANG_MAP.get(lang, RU).get(key, key)
