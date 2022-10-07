from fastapi import Request, Response
import json
from google.protobuf import json_format

NON_AUTH_PACKET = {"status": False, "info": "Non authed"}


async def create_answer(data: dict, buffer_type, return_object=False):
    answer_buffer = buffer_type()
    for el in data:
        setattr(answer_buffer, el, data[el])
        #print(type(getattr(answer_buffer, el)))
    #json_string = json.dumps(data)
    #json_format.Parse(json_string, answer_buffer)
    print(answer_buffer)


    if return_object:
        return answer_buffer
    answer_buffer_final = answer_buffer.SerializeToString()
    return Response(content=answer_buffer_final, media_type="application/protobuf")


async def nested_answer(data: list, main_buffer, inner_buffer):
    all_products = main_buffer()
    for product in range(len(data)):
        one_product = await create_answer(data[product], inner_buffer, return_object=True)
        all_products.product.append(one_product)
    data = all_products.SerializeToString()
    return Response(content=data, media_type="application/protobuf")

async def check_req_type(req: Request):
    req_type = "applciation/json"
    if "content-type" in req.headers:
        req_type = req.headers["content-type"]
    return req_type

async def parse_data(data, buffer_type):
    res_buffer = buffer_type()
    res_buffer.ParseFromString(data)
    return res_buffer
