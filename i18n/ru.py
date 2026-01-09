TEXTS = {
    "start": (
        "👋 <b>Добро пожаловать в byArto Analytics Bot!</b>\n\n"
        "🔎 Этот бот предоставляет <b>рыночную аналитику</b> для трейдеров.\n\n"
        "📊 <b>Доступные функции:</b>\n"
        "• Краткая сводка рынка\n"
        "• Важные рыночные события\n"
        "• Рыночная активность\n"
        "• Аномальная волатильность\n"
        "• Перетекание капитала (BTC ↔ альты)\n"
        "• Индикатор страха/жадности\n"
        "• Funding Rate (перегрев фьючерсов)\n"
        "• Long/Short Ratio\n\n"
        "📝 <b>Команды:</b>\n"
        "/summary — 📌 Краткая сводка рынка\n"
        "/events — Важные рыночные события\n"
        "/market — Рыночная активность\n"
        "/volatility — Аномальная волатильность\n"
        "/flow — Перетекание капитала\n"
        "/sentiment — Индикатор настроения\n"
        "/ratio — Long/Short Ratio\n"
        "/funding — Funding Rate\n"
        "/help — Справка\n"
        "/language — 🌐 Язык\n\n"
        "⚠️ <i>Бот НЕ даёт торговых сигналов, только данные для анализа</i>"
    ),

    "help": (
        "📚 <b>Справка по боту</b>\n\n"
        "Бот предоставляет аналитические данные по рынку криптовалют.\n\n"
        "<b>Команды:</b>\n"
        "/summary — Краткая сводка рынка\n"
        "/events — Важные события\n"
        "/market — Рыночная активность\n"
        "/volatility — Волатильность\n"
        "/flow — Потоки капитала\n"
        "/sentiment — Страх / Жадность\n"
        "/ratio — Long/Short\n"
        "/funding — Funding Rate\n"
        "/language — Сменить язык"
    ),

    # 🌐 Language
    "choose_language": "🌐 Выберите язык:",
    "language_changed": "✅ Язык успешно изменён",

    # ⏳ Loaders
    "loading_market": "⏳ Загружаю данные о рыночной активности...",
    "loading_volatility": "⏳ Анализирую волатильность...",
    "loading_flow": "⏳ Анализирую потоки капитала...",
    "loading_sentiment": "⏳ Рассчитываю настроение рынка...",
    "loading_ratio": "⏳ Анализирую Long/Short Ratio...",
    "loading_funding": "⏳ Анализирую funding rate...",
    "loading_events": "⏳ Загружаю важные события...",
    "loading_summary": "📊 Формирую краткую сводку рынка...",

    # ⚠️ Errors
    "error_generic": "⚠️ Произошла ошибка. Попробуйте позже.",
    # ===== SUMMARY =====
"summary_header": "📌 <b>КРАТКАЯ СВОДКА РЫНКА</b>",

"summary_total_cap": "Total Market Cap",
"summary_btc_dom": "BTC Dominance",

"summary_market_red_title": "🔴 <b>Рынок под давлением</b>",
"summary_market_red_desc": "Преобладает снижение по топ-активам.",

"summary_market_green_title": "🟢 <b>Рынок силы</b>",
"summary_market_green_desc": "Преобладает рост и покупательская активность.",

"summary_market_neutral_title": "⚪ <b>Рынок нейтрален</b>",
"summary_market_neutral_desc": "Баланс спроса и предложения.",

"summary_volatility_title": "⚡ <b>Аномальная волатильность</b>",
"summary_volatility_count": "Обнаружено монет",
"summary_volatility_none": "✅ <b>Аномальная волатильность:</b> не обнаружена",

"summary_growth": "Рост",
"summary_fall": "Падение",

"summary_events_title": "📰 <b>Важные события</b>",
"summary_events_none": "📰 <b>Важные события:</b> нет",

"summary_funding_title": "📉 <b>Фьючерсы (Funding Rate)</b>",

"summary_footer": (
    "🧠 Используйте эту сводку как контекст,\n"
    "а не как торговый сигнал."
),

"market_sentiment_bullish": "🟢 Повышенный интерес к риску",
"market_sentiment_bearish": "🔴 Преобладает давление продаж",
"market_sentiment_mixed": "🟡 Смешанная динамика рынка",
"volatility_header": "⚡ <b>АНОМАЛЬНАЯ ВОЛАТИЛЬНОСТЬ</b>",
"volatility_period": "⏰ <b>Последние 24 часа</b>",
"volatility_filter": "🔍 Анализ топ-50 | Фильтр: ≥$10M, ≥15%",
"volatility_calm": "✅ <b>Рынок спокоен</b>",
"volatility_no_anomalies": "• Нет значительных аномалий (>15%)",
"volatility_top50_ok": "• Топ-50 монет в пределах нормы",
"volatility_analyzed_50": "• Проанализировано: 50 монет",
"volatility_found": "🎯 <b>Обнаружено аномалий:</b>",
"volatility_context": "📊 <b>Контекст:</b>",
"volatility_mass_pump": "• 🟢 <b>Массовый рост</b> — капитал входит в рынок",
"volatility_mass_dump": "• 🔴 <b>Массовое падение</b> — фиксация прибыли",
"volatility_rotation": "• 🟡 <b>Ротация капитала</b>",
"volatility_local": "• 💡 <b>Локальные аномалии</b>",
"volatility_single_pump": "• 🚀 <b>Изолированный памп</b>",
"volatility_single_dump": "• 📉 <b>Изолированный дамп</b>",
"volatility_total_volume": "• Объём аномалий:",
# ===== EVENTS =====
"events_header": "📰 <b>Важные рыночные события</b>",
"events_intro": "Ниже перечислены события, которые могут повлиять на волатильность рынка.",
"date_unknown": "Дата уточняется",

"event_cpi_title": "CPI (Инфляция США)",
"event_cpi_desc": "Данные по инфляции часто вызывают резкие движения на рынках.",

"event_fomc_title": "FOMC (Решение ФРС по ставке)",
"event_fomc_desc": "Решения ФРС влияют на ликвидность и риск-аппетит.",

"event_apt_unlock_title": "Разблокировка токенов: APT",
"event_apt_unlock_desc": "Разблокировки увеличивают предложение и могут усилить давление.",

"event_eth_update_title": "Обновление сети Ethereum",
"event_eth_update_desc": "Крупные апдейты могут влиять на ожидания рынка.",

"event_tomorrow": "Завтра",
"event_in_2_days": "Через 2 дня",
"event_this_week": "На этой неделе",
"market_activity_header": "📊 <b>РЫНОЧНАЯ АКТИВНОСТЬ</b>",
"market_activity_period": "⏰ <i>Последние 24 часа</i>",
"market_activity_top_volume": "🔝 <b>Futures — топ по объёму:</b>",
"market_activity_context_title": "📈 <b>Контекст рынка:</b>",
"market_activity_note": "💡 <i>Объёмы показывают интерес, не направление</i>",
"market_activity_sentiment_risk_on": "🟢 Повышенный интерес к риску",
"market_activity_sentiment_sell_pressure": "🔴 Преобладает давление продаж",
"market_activity_sentiment_mixed": "🟡 Смешанная динамика рынка",
"updated_at": "⏱ Обновлено:",

# ===== FUNDING RATE =====
"funding_header": "📉 <b>Фьючерсы (Funding Rate)</b>",
"funding_unavailable": "⚠️ Данные недоступны",

"funding_long_overheat_title": "🔴 <b>Перегрев лонгов</b>",
"funding_long_overheat_desc": "Толпа перегружена в покупках.",

"funding_short_overheat_title": "🟢 <b>Перегрев шортов</b>",
"funding_short_overheat_desc": "Высокий риск short squeeze.",

"funding_neutral_title": "⚪ <b>Нейтрально</b>",
"funding_neutral_desc": "Баланс между лонгами и шортами.",
"ratio_header": "⚖️ <b>LONG / SHORT RATIO</b>",
"ratio_subheader": "📊 Где находится толпа",
"ratio_bias_long": "Перекос в LONG",
"ratio_bias_short": "Перекос в SHORT",
"ratio_bias_neutral": "Баланс",

"ratio_analysis_title": "🧠 <b>Анализ толпы:</b>",
"ratio_analysis_long": "• 🟢 Толпа перекошена в LONG\n  └ Риск ликвидации лонгов",
"ratio_analysis_short": "• 🔴 Толпа перекошена в SHORT\n  └ Риск ликвидации шортов",
"ratio_analysis_neutral": "• 🟡 Рынок сбалансирован",

"ratio_long_count": "Монет с перекосом в Long",
"ratio_short_count": "Монет с перекосом в Short",
"ratio_neutral_count": "Балансированных",

"loading_flow": "⏳ Анализирую потоки капитала...",
"loading_sentiment": "⏳ Рассчитываю настроение рынка...",
"loading_ratio": "⏳ Анализирую Long/Short Ratio...",
"loading_funding": "⏳ Анализирую funding rate...",

 # ===== FLOW =====
"flow_header": "💰 <b>ПЕРЕТЕКАНИЕ КАПИТАЛА</b>",
"flow_period": "⏰ <b>Последние 24 часа</b>",
"flow_dynamics": "📊 <b>Динамика:</b>",
"flow_alts_avg": "Топ-20 альтов (среднее)",
"flow_alts_volume": "Объём альтов",
"flow_analysis": "🔄 <b>Анализ потока:</b>",

"flow_sync_growth": "• 🟢 <b>Рынок растёт синхронно</b>\n  └ BTC и альты движутся вместе вверх",
"flow_sync_drop": "• 🔴 <b>Общая коррекция рынка</b>\n  └ BTC и альты падают вместе",
"flow_calm": "• 🟡 <b>Спокойное состояние</b>\n  └ Нет значимых движений",

"flow_into_alts": "• 🚀 <b>Капитал течёт В АЛЬТЫ</b>\n  └ Альты опережают BTC",
"flow_into_btc": "• 🛡️ <b>Капитал течёт В BTC</b>\n  └ BTC опережает альты",

"flow_soft_alts": "• 💚 <b>Умеренный интерес к альтам</b>",
"flow_soft_btc": "• 🔵 <b>Умеренная защита в BTC</b>",
"flow_diff": "Разница:",
"flow_top_gainers": "🏆 <b>Топ-3 альта по росту:</b>",

"updated_at": "⏱ Обновлено:",

# ===== FEAR & GREED =====
"fg_header": "ИНДИКАТОР СТРАХА И ЖАДНОСТИ",
"fg_score": "Текущий уровень",
"fg_status": "Статус",
"fg_stats": "Рыночная статистика",

"fg_extreme_greed": "Экстремальная жадность",
"fg_extreme_greed_desc": "Рынок перегрет, высок риск коррекции",

"fg_greed": "Жадность",
"fg_greed_desc": "Оптимизм преобладает",

"fg_neutral": "Нейтрально",
"fg_neutral_desc": "Рынок в балансе",

"fg_fear": "Страх",
"fg_fear_desc": "Участники действуют осторожно",

"fg_extreme_fear": "Экстремальный страх",
"fg_extreme_fear_desc": "Паника на рынке, возможны возможности",

"fg_positive": "В росте",
"fg_negative": "В падении",
"fg_volatility": "Средняя волатильность",

}

