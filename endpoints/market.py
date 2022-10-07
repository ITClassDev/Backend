from fastapi import APIRouter, Depends, Request, Response
from repositories.market import MarketRepository
from .depends import get_market_repository
from fastapi.encoders import jsonable_encoder
from core.utils import check_req_type, create_answer_from_dict, create_answer
import pbs.main_pb2 as MainBuffer

router = APIRouter()

@router.get("/all")
async def get_all_products(market_rep: MarketRepository = Depends(get_market_repository), request: Request = Request):
    req_type = await check_req_type(request)
    data = await market_rep.get_all_products()
    data = jsonable_encoder(data)
    if req_type == "application/protobuf":
        all_products = MainBuffer.MarketProducts()
        #data = await create_answer_from_dict(data, MainBuffer.MarketProducts)
        
        for product in range(len(data)):
            one_product = await create_answer(data[product], MainBuffer.MarketProduct, return_object=True)
            all_products.product.append(one_product)
        data = all_products.SerializeToString()
        data = Response(content=data, media_type="application/protobuf")
        
    return data