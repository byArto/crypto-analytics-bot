import aiohttp
import config

class BinanceClient:
    """
    Клиент для работы с Binance Futures API
    
    Этот класс будет использоваться в будущих модулях
    для более сложных запросов к бирже
    """
    
    def __init__(self):
        self.base_url = config.BINANCE_FUTURES_API
        self.session = None
    
    async def __aenter__(self):
        """Создаём сессию при входе в контекст"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Закрываем сессию при выходе из контекста"""
        if self.session:
            await self.session.close()
    
    async def get_24h_ticker(self):
        """Получить данные за 24 часа по всем парам"""
        url = f"{self.base_url}/fapi/v1/ticker/24hr"
        async with self.session.get(url) as response:
            return await response.json()
    
    async def get_funding_rate(self, symbol: str = None):
        """Получить funding rate (будет использоваться в следующих модулях)"""
        url = f"{self.base_url}/fapi/v1/fundingRate"
        params = {'symbol': symbol} if symbol else {}
        async with self.session.get(url, params=params) as response:
            return await response.json()