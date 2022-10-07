from db.market import market
from .base import BaseRepository
from models.market import MarketProducts


class MarketRepository(BaseRepository):
    async def get_all_products(self) -> list:
        query = market.select()
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, product_id) -> dict:
        query = market.select().where(market.c.id == product_id)
        product = await self.database.fetch_one(query)
        if product is None:
            return None
        return MarketProducts.parse_obj(product)

    async def add(self, prod: MarketProducts) -> int:
        values = {**prod.dict()}
        values.pop("id", None)
        query = market.insert().values(**values)
        product_id = await self.database.execute(query)  # Created product id
        return product_id
