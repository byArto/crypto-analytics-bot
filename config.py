import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()
COINGLASS_API_KEY = os.getenv("COINGLASS_API_KEY")

# Telegram настройки
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# BingX настройки
BINGX_REF_LINK = os.getenv('BINGX_REF_LINK', 'https://bingx.com')
SHOW_REF_BUTTON = os.getenv('SHOW_REF_BUTTON', 'true').lower() == 'true'
REF_BUTTON_FREQUENCY = int(os.getenv('REF_BUTTON_FREQUENCY', 3))

# Binance API endpoints (публичные, не требуют ключей)
BINANCE_FUTURES_API = 'https://fapi.binance.com'

# Настройки авто-алертов
ALERT_CHAT_ID = int(os.getenv('ALERT_CHAT_ID')) # ID чата для алертов
ALERT_CHECK_INTERVAL = int(os.getenv('ALERT_CHECK_INTERVAL', 15))  # Минут между проверками (по умолчанию 15)
ENABLE_AUTO_ALERTS = os.getenv('ENABLE_AUTO_ALERTS', 'true').lower() == 'true'  # Включить/выключить авто-алерты

# Валидация токена
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN не найден в .env файле!")
