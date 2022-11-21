from fastapi import Request, Response
from google.protobuf.json_format import MessageToDict
from pydantic import create_model


async def create_answer(data: dict, buffer_type, return_object=False):
    answer_buffer = buffer_type()
    for el in data:
        if data[el] != None:
            setattr(answer_buffer, el, data[el])

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


async def parse_data(data, buffer_type):
    res_buffer = buffer_type()
    res_buffer.ParseFromString(data)
    return res_buffer


async def parse_to_object(data, object_class, buffer_type):
    data = MessageToDict(await parse_data(data, buffer_type))
    return object_class(**data)
