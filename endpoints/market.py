from fastapi import APIRouter, Depends, Request
from repositories.market import MarketRepository
from .depends import get_market_repository
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.get("/all")
async def get_all_products(market_rep: MarketRepository = Depends(get_market_repository), request: Request = Request):
    req_type = await check_req_type(request)
    data = await market_rep.get_all_products()
    data = jsonable_encoder(data)
    if req_type == "application/protobuf":
        return_data = await create_answer(return_data, MainBuffer.UserData)
