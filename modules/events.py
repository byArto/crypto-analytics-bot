from datetime import datetime
from core.i18n import t

# События, по которым уже отправляли алерт
ALERTED_EVENTS = set()
ALERTED_30MIN_EVENTS = set()

# Важные рыночные события (ручной список)
EVENTS = [
    {
        "id": "cpi",
        "title_key": "event_cpi_title",
        "type": "macro",
        "datetime_utc": "2026-01-08 16:30",
        "importance": "high",
        "desc_key": "event_cpi_desc",
    },
    {
        "id": "fomc",
        "title_key": "event_fomc_title",
        "type": "macro",
        "date_key": "event_tomorrow",
        "importance": "high",
        "desc_key": "event_fomc_desc",
    },
    {
        "id": "apt_unlock",
        "title_key": "event_apt_unlock_title",
        "type": "unlock",
        "date_key": "event_in_2_days",
        "importance": "medium",
        "desc_key": "event_apt_unlock_desc",
    },
    {
        "id": "eth_update",
        "title_key": "event_eth_update_title",
        "type": "crypto",
        "date_key": "event_this_week",
        "importance": "medium",
        "desc_key": "event_eth_update_desc",
    },
]

IMPORTANCE_EMOJI = {
    "high": "🔴",
    "medium": "🟠",
    "low": "🟢",
}


async def get_events_summary(user_id: int):
    """
    Сводка важных рыночных событий (локализовано)
    """
    now = datetime.utcnow().strftime("%H:%M UTC")
    lines = []

    for event in EVENTS:
        emoji = IMPORTANCE_EMOJI.get(event["importance"], "ℹ️")

        date_text = (
            event.get("datetime_utc")
            or t(user_id, event.get("date_key"))
            or t(user_id, "date_unknown")
        )

        lines.append(
            f"{emoji} <b>{t(user_id, event['title_key'])}</b>\n"
            f"📅 {date_text}\n"
            f"ℹ️ {t(user_id, event['desc_key'])}\n"
        )

    message = (
        f"{t(user_id, 'events_header')}\n\n"
        f"{t(user_id, 'events_intro')}\n\n"
        + "\n".join(lines) +
        f"\n⏱ {t(user_id, 'updated_at')} {now}"
    )

    return message


async def get_high_importance_events_for_alert():
    """
    High-importance события (один раз)
    """
    events_for_alert = []

    for event in EVENTS:
        if event["importance"] != "high":
            continue

        if event["id"] in ALERTED_EVENTS:
            continue

        events_for_alert.append(event)
        ALERTED_EVENTS.add(event["id"])

    return events_for_alert


async def get_events_30min_before_alert():
    """
    High-importance события за ~30 минут до выхода
    """
    now = datetime.utcnow()
    alerts = []

    for event in EVENTS:
        if event["importance"] != "high":
            continue

        if "datetime_utc" not in event:
            continue

        if event["id"] in ALERTED_30MIN_EVENTS:
            continue

        event_time = datetime.strptime(
            event["datetime_utc"],
            "%Y-%m-%d %H:%M"
        )

        delta_minutes = (event_time - now).total_seconds() / 60

        if 25 <= delta_minutes <= 35:
            alerts.append(event)
            ALERTED_30MIN_EVENTS.add(event["id"])

    return alerts
