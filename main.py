import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.handlers import register_handlers
import config
from scheduler import setup_scheduler

# Настройка логирования (чтобы видеть что происходит)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Главная функция запуска бота"""
    
    logger.info("🔧 Инициализация бота...")
    
    # Создаём бота с токеном из config.py
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    
    # Регистрируем все команды (/start, /market и т.д.)
    register_handlers(dp)
    
    # Настраиваем планировщик для авто-алертов
    scheduler = setup_scheduler(bot)
    
    # Запускаем планировщик
    if config.ENABLE_AUTO_ALERTS:
        scheduler.start()
        logger.info("✅ Авто-алерты включены")
    else:
        logger.info("⚠️ Авто-алерты отключены")
    
    logger.info("🚀 Бот успешно запущен! Жду команды в Telegram...")
    
    try:
        # Удаляем старые обновления и запускаем бота
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
    finally:
        # Останавливаем планировщик при выходе
        if scheduler.running:
            scheduler.shutdown()
            logger.info("⏰ Планировщик остановлен")
        
        await bot.session.close()
        logger.info("🛑 Бот остановлен")

if __name__ == '__main__':
    # Запускаем бота
    asyncio.run(main())