import time
import json
import aiohttp
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from core.i18n import t

# Кэш событий
EVENTS_CACHE: List[Dict] = []
CACHE_TIMESTAMP: float = 0
CACHE_TTL: int = 21600  # 6 часов

# Персистентное хранилище для отправленных алертов
ALERTS_FILE = Path("data/alerted_events.json")
ALERTS_30MIN_FILE = Path("data/alerted_30min_events.json")

IMPORTANCE_EMOJI = {
    "high": "🔴",
    "medium": "🟠",
    "low": "🟢",
}


def load_alerted_events(file_path: Path) -> set:
    """Загружает список отправленных оповещений из файла"""
    try:
        if file_path.exists():
            return set(json.loads(file_path.read_text()))
    except Exception:
        pass
    return set()


def save_alerted_events(events: set, file_path: Path):
    """Сохраняет список отправленных оповещений в файл"""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(list(events), indent=2))
    except Exception:
        pass


# Инициализация при старте модуля
ALERTED_EVENTS = load_alerted_events(ALERTS_FILE)
ALERTED_30MIN_EVENTS = load_alerted_events(ALERTS_30MIN_FILE)


async def fetch_static_crypto_events() -> List[Dict]:
    """
    Возвращает статический список важных криптособытий.
    ПРИМЕЧАНИЕ: Этот список нужно обновлять вручную или через внешний источник.

    В будущем можно подключить платный API (CoinMarketCal Pro, LunarCrush)
    или парсить календари типа CoinGecko Events, Token Unlocks, и т.д.
    """

    # Получаем текущую дату
    now = datetime.utcnow()

    # Важные предстоящие события (обновляйте этот список периодически)
    static_events = [
        {
            "title": "Bitcoin Halving (April 2024)",
            "description": "Bitcoin block reward reduction from 6.25 to 3.125 BTC. Historically leads to bull markets.",
            "start_date": "2024-04-15T00:00:00.000Z",
            "type": "Event",
            "importance_keywords": ["halving", "bitcoin"],
        },
        {
            "title": "Ethereum Pectra Upgrade (Q1 2024)",
            "description": "Major Ethereum network upgrade including account abstraction improvements.",
            "start_date": "2024-03-01T00:00:00.000Z",
            "type": "Event",
            "importance_keywords": ["upgrade", "ethereum"],
        },
        {
            "title": "Token Unlock: APT (Monthly)",
            "description": "Aptos token unlock - approximately 11.3M APT tokens unlocked monthly.",
            "start_date": (now + timedelta(days=10)).strftime("%Y-%m-%dT12:00:00.000Z"),
            "type": "Event",
            "importance_keywords": ["unlock", "aptos"],
        },
        {
            "title": "US Federal Reserve FOMC Meeting",
            "description": "Federal Open Market Committee meeting - interest rate decision affects crypto markets.",
            "start_date": (now + timedelta(days=20)).strftime("%Y-%m-%dT18:00:00.000Z"),
            "type": "Event",
            "importance_keywords": ["fomc", "fed"],
        },
        {
            "title": "US CPI Data Release",
            "description": "Consumer Price Index (inflation data) - typically causes market volatility.",
            "start_date": (now + timedelta(days=7)).strftime("%Y-%m-%dT13:30:00.000Z"),
            "type": "Event",
            "importance_keywords": ["cpi", "inflation"],
        },
    ]

    # Фильтруем только будущие события
    future_events = []
    for event in static_events:
        try:
            event_dt = datetime.fromisoformat(event["start_date"].replace("Z", "+00:00"))
            if event_dt > now.replace(tzinfo=event_dt.tzinfo):
                future_events.append(event)
        except Exception:
            continue

    return future_events


async def fetch_coingecko_events() -> List[Dict]:
    """
    Попытка получить события из CoinGecko API (резервный метод).
    ПРИМЕЧАНИЕ: Этот эндпоинт может быть недоступен в бесплатной версии API.
    """
    # Пока CoinGecko Events API недоступен в бесплатной версии
    # Возвращаем пустой список и полагаемся на статические события
    return []


def normalize_events(raw_events: List[Dict]) -> List[Dict]:
    """
    Преобразует события из CoinGecko в унифицированный формат бота.

    Формат CoinGecko event:
    {
        "title": "...",
        "description": "...",
        "start_date": "2026-01-20T00:00:00.000Z",
        "end_date": "2026-01-20T23:59:59.999Z",
        "type": "Event",
        "website": "...",
        "screenshot": "...",
    }

    Формат бота:
    {
        "id": str,
        "title": str,
        "type": str,
        "datetime_utc": str,
        "importance": str,
        "description": str
    }
    """
    normalized = []

    for raw_event in raw_events:
        try:
            # Парсим дату начала события
            start_date_str = raw_event.get("start_date", "")
            if not start_date_str:
                continue

            # Формат: "2026-01-20T00:00:00.000Z"
            event_dt = datetime.fromisoformat(start_date_str.replace("Z", "+00:00"))

            # Пропускаем прошедшие события
            if event_dt < datetime.utcnow().replace(tzinfo=event_dt.tzinfo):
                continue

            title = raw_event.get("title", "").strip()
            description = raw_event.get("description", "").strip()

            if not title:
                continue

            # Определяем важность на основе ключевых слов
            importance = determine_importance(title, description)

            # Определяем тип события
            event_type = determine_event_type(title, description)

            # Создаем уникальный ID
            event_id = f"cg_{raw_event.get('title', '')}_{event_dt.strftime('%Y%m%d')}"[:50]

            normalized.append({
                "id": event_id,
                "title": title,
                "type": event_type,
                "datetime_utc": event_dt.strftime("%Y-%m-%d %H:%M"),
                "importance": importance,
                "description": description[:200] if description else title,  # Ограничиваем длину
            })
        except Exception:
            # Пропускаем события с ошибками парсинга
            continue

    # Сортируем по дате (ближайшие первые)
    normalized.sort(key=lambda e: e["datetime_utc"])

    # Ограничиваем количество (берем топ-20 ближайших)
    return normalized[:20]


def determine_importance(title: str, description: str) -> str:
    """
    Определяет важность события на основе ключевых слов.
    """
    text = (title + " " + description).lower()

    # Высокая важность: макро-события, крупные обновления, листинги, хардфорки
    high_keywords = [
        "mainnet launch", "hard fork", "halving", "binance listing",
        "coinbase listing", "major upgrade", "token burn", "airdrop",
        "fomc", "fed", "cpi", "inflation", "federal reserve", "interest rate"
    ]

    # Средняя важность: анлоки, обновления, AMA
    medium_keywords = [
        "unlock", "vesting", "token release", "update", "upgrade",
        "ama", "partnership", "integration"
    ]

    for keyword in high_keywords:
        if keyword in text:
            return "high"

    for keyword in medium_keywords:
        if keyword in text:
            return "medium"

    return "low"


def determine_event_type(title: str, description: str) -> str:
    """
    Определяет тип события (macro, token, network).
    """
    text = (title + " " + description).lower()

    if any(kw in text for kw in ["unlock", "vesting", "token release", "airdrop"]):
        return "unlock"

    if any(kw in text for kw in ["mainnet", "upgrade", "hard fork", "network", "chain"]):
        return "network"

    return "token"


async def get_events() -> List[Dict]:
    """
    Возвращает актуальные события (из кэша или источников).
    Кэш обновляется каждые 6 часов.

    Источники событий (в порядке приоритета):
    1. Статический список важных событий (fetch_static_crypto_events)
    2. CoinGecko API (если доступен)
    3. Кэш из предыдущих запросов
    """
    global EVENTS_CACHE, CACHE_TIMESTAMP

    # Проверяем кэш
    current_time = time.time()
    if current_time - CACHE_TIMESTAMP < CACHE_TTL and EVENTS_CACHE:
        return EVENTS_CACHE

    # Обновляем из источников
    try:
        # Приоритет 1: Статические события
        static_events = await fetch_static_crypto_events()

        # Приоритет 2: CoinGecko API (если вдруг заработает)
        api_events = await fetch_coingecko_events()

        # Комбинируем события
        all_events = static_events + api_events

        if all_events:
            EVENTS_CACHE = normalize_events(all_events)
            CACHE_TIMESTAMP = current_time
        elif not EVENTS_CACHE:
            # Если нет событий и кэш пуст, возвращаем пустой список
            EVENTS_CACHE = []
    except Exception:
        # При ошибке возвращаем старый кэш (если есть)
        pass

    return EVENTS_CACHE


async def get_events_summary(user_id: int) -> str:
    """
    Сводка важных рыночных событий (локализовано).
    """
    events = await get_events()
    now = datetime.utcnow().strftime("%H:%M UTC")

    if not events:
        return f"{t(user_id, 'events_header')}\n\n{t(user_id, 'event_no_events')}\n\n⏱ {t(user_id, 'updated_at')} {now}"

    lines = []
    for event in events:
        emoji = IMPORTANCE_EMOJI.get(event["importance"], "ℹ️")

        lines.append(
            f"{emoji} <b>{event['title']}</b>\n"
            f"📅 {event['datetime_utc']} UTC\n"
            f"ℹ️ {event['description']}\n"
        )

    message = (
        f"{t(user_id, 'events_header')}\n\n"
        f"{t(user_id, 'events_intro')}\n\n"
        + "\n".join(lines) +
        f"\n⏱ {t(user_id, 'updated_at')} {now}"
    )

    return message


async def get_high_importance_events_for_alert() -> List[Dict]:
    """
    Возвращает high-importance события для алерта (только один раз для каждого).
    """
    events = await get_events()
    events_for_alert = []

    for event in events:
        if event["importance"] != "high":
            continue

        if event["id"] in ALERTED_EVENTS:
            continue

        events_for_alert.append(event)
        ALERTED_EVENTS.add(event["id"])

    # Сохраняем обновленный список алертов
    if events_for_alert:
        save_alerted_events(ALERTED_EVENTS, ALERTS_FILE)

    return events_for_alert


async def get_events_30min_before_alert() -> Optional[str]:
    """
    Возвращает текст алерта для событий за 25-35 минут до начала.
    Возвращает None если нет событий для алерта.
    """
    events = await get_events()
    now = datetime.utcnow()
    alerts = []

    for event in events:
        if event["importance"] != "high":
            continue

        if event["id"] in ALERTED_30MIN_EVENTS:
            continue

        try:
            event_time = datetime.strptime(event["datetime_utc"], "%Y-%m-%d %H:%M")
            delta_minutes = (event_time - now).total_seconds() / 60

            if 25 <= delta_minutes <= 35:
                alerts.append(event)
                ALERTED_30MIN_EVENTS.add(event["id"])
        except Exception:
            continue

    # Сохраняем обновленный список 30-мин алертов
    if alerts:
        save_alerted_events(ALERTED_30MIN_EVENTS, ALERTS_30MIN_FILE)

        # Формируем текст алерта
        lines = []
        for event in alerts:
            lines.append(
                f"🔴 <b>{event['title']}</b>\n"
                f"📅 {event['datetime_utc']} UTC\n"
                f"ℹ️ {event['description']}\n"
            )

        return (
            "⚠️ <b>Important Event Alert (30 min before)</b>\n\n" +
            "\n".join(lines)
        )

    return None
