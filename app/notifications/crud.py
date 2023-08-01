from sqlmodel.ext.asyncio.session import AsyncSession

class NotificationsCRUD:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def create(self, data):
        pass