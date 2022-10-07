from db.market import market
from .base import BaseRepository
from models.market import MarketProducts

class MarketRepository(BaseRepository):
    async def get_all_products(self) -> list:
        query = market.select()
        return await self.database.fetch_all(query=query)