from pydantic import BaseModel
from typing import Optional

class MarketProducts(BaseModel):
    id: Optional[int] = None
    title: str
    cost: int
    remain_amount: int
    about: str
    image_path: str