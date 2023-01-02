from db.oauth_tokens import oauth_tokens
from .base import BaseRepository
from models.oauth_tokens import OauthToken

class OAuthTokensRepository(BaseRepository):
    async def get_by_token(self, token: str) -> OauthToken:
        query = oauth_tokens.select().where(oauth_tokens.c.token == token)
        return await self.database.fetch_one(query)

    async def save_token(self, t: OauthToken) -> None:
        values = {**t.dict()}
        values.pop("entry_id", None)
        query = oauth_tokens.insert().values(**values)
        await self.database.execute(query)
    
    async def expire_token(self, token: str) -> None:
        query = oauth_tokens.delete().where(oauth_tokens.c.token == token)
        await self.database.execute(query)

    async def expire_all(self, app_id: int) -> None:
        query = oauth_tokens.delete().where(oauth_tokens.c.app_id == app_id)
        await self.database.execute(query)