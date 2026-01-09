TEXTS = {
    "start": (
        "👋 <b>Welcome to byArto Analytics Bot!</b>\n\n"
        "🔎 This bot provides <b>crypto market analytics</b> for traders.\n\n"
        "📊 <b>Available features:</b>\n"
        "• Market summary\n"
        "• Important market events\n"
        "• Market activity\n"
        "• Abnormal volatility\n"
        "• Capital flow (BTC ↔ alts)\n"
        "• Fear & Greed index\n"
        "• Funding Rate (futures overheating)\n"
        "• Long/Short Ratio\n\n"
        "📝 <b>Commands:</b>\n"
        "/summary — 📌 Market summary\n"
        "/events — Important market events\n"
        "/market — Market activity\n"
        "/volatility — Abnormal volatility\n"
        "/flow — Capital flow\n"
        "/sentiment — Market sentiment\n"
        "/ratio — Long/Short Ratio\n"
        "/funding — Funding Rate\n"
        "/help — Help\n"
        "/language — 🌐 Language\n\n"
        "⚠️ <i>This bot does NOT provide trading signals</i>"
    ),

    "help": (
        "📚 <b>Bot help</b>\n\n"
        "This bot provides crypto market analytics.\n\n"
        "<b>Commands:</b>\n"
        "/summary — Market summary\n"
        "/events — Important events\n"
        "/market — Market activity\n"
        "/volatility — Volatility\n"
        "/flow — Capital flow\n"
        "/sentiment — Fear & Greed\n"
        "/ratio — Long/Short\n"
        "/funding — Funding Rate\n"
        "/language — Change language"
    ),

    # 🌐 Language
    "choose_language": "🌐 Choose language:",
    "language_changed": "✅ Language updated",

    # ⏳ Loaders
    "loading_market": "⏳ Loading market activity...",
    "loading_volatility": "⏳ Analyzing volatility...",
    "loading_flow": "⏳ Analyzing capital flows...",
    "loading_sentiment": "⏳ Calculating market sentiment...",
    "loading_ratio": "⏳ Analyzing Long/Short Ratio...",
    "loading_funding": "⏳ Analyzing funding rates...",
    "loading_events": "⏳ Loading important events...",
    "loading_summary": "📊 Building market summary...",

    # ⚠️ Errors
    "error_generic": "⚠️ An error occurred. Please try again later.",
    # ===== SUMMARY =====
"summary_header": "📌 <b>MARKET SUMMARY</b>",

"summary_total_cap": "Total Market Cap",
"summary_btc_dom": "BTC Dominance",

"summary_market_red_title": "🔴 <b>Market under pressure</b>",
"summary_market_red_desc": "Decline dominates across top assets.",

"summary_market_green_title": "🟢 <b>Market strength</b>",
"summary_market_green_desc": "Growth and buyer activity dominate.",

"summary_market_neutral_title": "⚪ <b>Market neutral</b>",
"summary_market_neutral_desc": "No clear dominance between buyers and sellers.",

"summary_volatility_title": "⚡ <b>Abnormal volatility</b>",
"summary_volatility_count": "Coins detected",
"summary_volatility_none": "✅ <b>Abnormal volatility:</b> not detected",

"summary_growth": "Growth",
"summary_fall": "Decline",

"summary_events_title": "📰 <b>Important events</b>",
"summary_events_none": "📰 <b>Important events:</b> none",

"summary_funding_title": "📉 <b>Futures (Funding Rate)</b>",

"summary_footer": (
    "🧠 Use this summary as market context,\n"
    "not as a trading signal."
),

"market_sentiment_bullish": "🟢 Increased risk appetite",
"market_sentiment_bearish": "🔴 Selling pressure dominates",
"market_sentiment_mixed": "🟡 Mixed market dynamics",
"volatility_header": "⚡ <b>ABNORMAL VOLATILITY</b>",
"volatility_period": "⏰ <b>Last 24 hours</b>",
"volatility_filter": "🔍 Top-50 analysis | Filter: ≥$10M, ≥15%",
"volatility_calm": "✅ <b>Market is calm</b>",
"volatility_no_anomalies": "• No significant anomalies (>15%)",
"volatility_top50_ok": "• Top-50 coins within normal range",
"volatility_analyzed_50": "• Analyzed: 50 coins",
"volatility_found": "🎯 <b>Anomalies detected:</b>",
"volatility_context": "📊 <b>Context:</b>",
"volatility_mass_pump": "• 🟢 <b>Mass pump</b> — capital inflow",
"volatility_mass_dump": "• 🔴 <b>Mass dump</b> — profit taking",
"volatility_rotation": "• 🟡 <b>Capital rotation</b>",
"volatility_local": "• 💡 <b>Local anomalies</b>",
"volatility_single_pump": "• 🚀 <b>Isolated pump</b>",
"volatility_single_dump": "• 📉 <b>Isolated dump</b>",
"volatility_total_volume": "• Anomaly volume:",
# ===== EVENTS =====
"events_header": "📰 <b>Important market events</b>",
"events_intro": "Below are events that may affect market volatility.",
"date_unknown": "Date to be confirmed",

"event_cpi_title": "CPI (US Inflation)",
"event_cpi_desc": "Inflation data often triggers sharp market moves.",

"event_fomc_title": "FOMC (Fed interest rate decision)",
"event_fomc_desc": "Fed decisions affect liquidity and risk appetite.",

"event_apt_unlock_title": "Token unlock: APT",
"event_apt_unlock_desc": "Unlocks increase supply and may add selling pressure.",

"event_eth_update_title": "Ethereum network upgrade",
"event_eth_update_desc": "Major upgrades can affect market expectations.",

"event_tomorrow": "Tomorrow",
"event_in_2_days": "In 2 days",
"event_this_week": "This week",
"market_activity_header": "📊 <b>MARKET ACTIVITY</b>",
"market_activity_period": "⏰ <i>Last 24 hours</i>",
"market_activity_top_volume": "🔝 <b>Futures — top by volume:</b>",
"market_activity_context_title": "📈 <b>Market context:</b>",
"market_activity_note": "💡 <i>Volume shows interest, not direction</i>",
"market_activity_sentiment_risk_on": "🟢 Increased risk appetite",
"market_activity_sentiment_sell_pressure": "🔴 Selling pressure dominates",
"market_activity_sentiment_mixed": "🟡 Mixed market dynamics",
"updated_at": "⏱ Updated:",

# ===== FUNDING RATE =====
"funding_header": "📉 <b>Futures (Funding Rate)</b>",
"funding_unavailable": "⚠️ Data unavailable",

"funding_long_overheat_title": "🔴 <b>Longs overheated</b>",
"funding_long_overheat_desc": "Crowd is overloaded on the long side.",

"funding_short_overheat_title": "🟢 <b>Shorts overheated</b>",
"funding_short_overheat_desc": "High risk of a short squeeze.",

"funding_neutral_title": "⚪ <b>Neutral</b>",
"funding_neutral_desc": "Balance between longs and shorts.",
"ratio_header": "⚖️ <b>LONG / SHORT RATIO</b>",
"ratio_subheader": "📊 Crowd positioning",
"ratio_bias_long": "Long bias",
"ratio_bias_short": "Short bias",
"ratio_bias_neutral": "Balanced",

"ratio_analysis_title": "🧠 <b>Crowd analysis:</b>",
"ratio_analysis_long": "• 🟢 Crowd heavily LONG\n  └ Risk of long liquidations",
"ratio_analysis_short": "• 🔴 Crowd heavily SHORT\n  └ Risk of short squeeze",
"ratio_analysis_neutral": "• 🟡 Market balanced",

"ratio_long_count": "Long-biased coins",
"ratio_short_count": "Short-biased coins",
"ratio_neutral_count": "Balanced coins",

# ===== FLOW =====
"flow_header": "💰 <b>CAPITAL FLOW</b>",
"flow_period": "⏰ <b>Last 24 hours</b>",
"flow_dynamics": "📊 <b>Dynamics:</b>",
"flow_alts_avg": "Top-20 alts (average)",
"flow_alts_volume": "Altcoins volume",
"flow_analysis": "🔄 <b>Flow analysis:</b>",

"flow_sync_growth": "• 🟢 <b>Synchronized market growth</b>\n  └ BTC and alts rising together",
"flow_sync_drop": "• 🔴 <b>Market-wide correction</b>\n  └ BTC and alts falling together",
"flow_calm": "• 🟡 <b>Calm market</b>\n  └ No significant movements",

"flow_into_alts": "• 🚀 <b>Capital flowing INTO ALTS</b>\n  └ Alts outperform BTC",
"flow_into_btc": "• 🛡️ <b>Capital flowing INTO BTC</b>\n  └ BTC outperforms alts",

"flow_soft_alts": "• 💚 <b>Moderate interest in alts</b>",
"flow_soft_btc": "• 🔵 <b>Moderate defensive positioning in BTC</b>",
"flow_diff": "Difference:",
"flow_top_gainers": "🏆 <b>Top-3 alt gainers:</b>",

"updated_at": "⏱ Updated:",

# ===== FEAR & GREED =====
"fg_header": "FEAR & GREED INDEX",
"fg_score": "Current score",
"fg_status": "Status",
"fg_stats": "Market statistics",

"fg_extreme_greed": "Extreme greed",
"fg_extreme_greed_desc": "Market is overheated, high risk of correction",

"fg_greed": "Greed",
"fg_greed_desc": "Optimism dominates the market",

"fg_neutral": "Neutral",
"fg_neutral_desc": "Market is balanced",

"fg_fear": "Fear",
"fg_fear_desc": "Participants are acting cautiously",

"fg_extreme_fear": "Extreme fear",
"fg_extreme_fear_desc": "Market panic, potential opportunities",

"fg_positive": "Positive coins",
"fg_negative": "Negative coins",
"fg_volatility": "Average volatility",

}
