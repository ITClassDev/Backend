from pydantic import BaseModel
from typing import Optional

class MarketProducts(BaseModel):
    id: Optional[int] = None
    title: str
    cost: int
    remainAmount: int
    about: str
    imagePath: str
