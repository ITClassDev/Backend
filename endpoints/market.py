from fastapi import APIRouter, Depends, Request, Response
from repositories.market import MarketRepository
from .depends import get_market_repository, get_current_user
from fastapi.encoders import jsonable_encoder
from core.utils import check_req_type, create_answer, nested_answer
import pbs.main_pb2 as MainBuffer
from models.user import User
from models.market import MarketProducts


router = APIRouter()


@router.get("/all")
async def get_all_products(market_rep: MarketRepository = Depends(get_market_repository), request: Request = Request):
    '''
    Input: None
    '''
    req_type = await check_req_type(request)
    data = await market_rep.get_all_products()
    data = jsonable_encoder(data)
    if req_type == "application/protobuf":
        data = await nested_answer(data, MainBuffer.MarketProducts, MainBuffer.MarketProduct)
    return data


@router.get("/{product_id}/info")
async def get_product_info(product_id: int, market_rep: MarketRepository = Depends(get_market_repository), request: Request = Request):
    '''
    Input:
    product_id: as a url param
    '''
    req_type = await check_req_type(request)
    data = await market_rep.get_by_id(product_id)
    if data:
        data = jsonable_encoder(data)
        data["status"] = True
        if req_type == "application/protobuf":
            data = await create_answer(data, MainBuffer.MarketProduct)
        return data

    data = {"status": False, "info": "no product with such id"}
    if req_type == "application/protobuf":
        data = await create_answer(data, MainBuffer.MarketProduct)

    return data


@router.post("/add")
async def add_new_product(current_user: User = Depends(get_current_user), request: Request = Request):
    '''
    Input:
    product_title: str
    product_cost: int
    product_about_text: str
    product_current_amount: int
    '''
    req_type = await check_req_type(request)
    if current_user and current_user.userRole == 1:  # Role 1 is admin role
        if req_type == "application/json":
            req_data = await request.json()
        else:
            buffer_data = await parse_data(await request.body(), MainBuffer.NewProduct)
            req_data = {"product_title": buffer_data.product_title, "product_cost": buffer_data.product_cost,
                        "product_about_text": buffer_data.product_about_text, "product_current_amount": buffer_data.product_current_amount}
        new_product_object = MarketProducts(title=req_data["product_title"], cost=req_data["product_cost"], remainAmount=req_data["product_current_amount"], about=req_data["product_about_text"], imagePath="def.png")
        print(new_product_object)
        return {"status": True}

    data = {"status": False, "info": "Low privilages"}
    if req_type == "application/protobuf":
        data = await create_answer(data, MainBuffer.MarketProduct)
    return data


@router.post("/{product_id}/buy")
async def buy_new_product():
    pass
