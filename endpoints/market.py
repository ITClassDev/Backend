from fastapi import APIRouter, Depends, Request, Response
from repositories.market import MarketRepository
from .depends import get_market_repository
from fastapi.encoders import jsonable_encoder
from core.utils import check_req_type, create_answer, nested_answer
import pbs.main_pb2 as MainBuffer

router = APIRouter()

@router.get("/all")
async def get_all_products(market_rep: MarketRepository = Depends(get_market_repository), request: Request = Request):
    req_type = await check_req_type(request)
    data = await market_rep.get_all_products()
    data = jsonable_encoder(data)
    if req_type == "application/protobuf":
        data = await nested_answer(data, MainBuffer.MarketProducts, MainBuffer.MarketProduct)
    return data

@router.get("/{product_id}/info")
async def get_product_info(product_id: int, market_rep: MarketRepository = Depends(get_market_repository), request: Request = Request):
    req_type = await check_req_type(request)
    data = await market_rep.get_by_id(product_id)
    if data:
        data = jsonable_encoder(data)
        data["status"] = True
        if req_type == "application/protobuf":
            data = await create_answer(data, MainBuffer.MarketProduct)
    else:
        data = {"status": False, "info": "no product with such id"}
        if req_type == "application/protobuf":
            data = await create_answer(data, MainBuffer.MarketProduct)

    return data