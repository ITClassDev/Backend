from fastapi import Request, Response
from google.protobuf.json_format import MessageToDict
from pydantic import create_model
import time
import random
import string
import os

NON_AUTH_PACKET = {"status": False, "info": "Non authed"}

async def get_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))



async def create_answer(data: dict, buffer_type, return_object=False):
    answer_buffer = buffer_type()
    for el in data:
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

# Deprecated
async def check_req_type(req: Request):
    req_type = "applciation/json"
    if "content-type" in req.headers:
        req_type = req.headers["content-type"]
    return req_type


async def parse_data(data, buffer_type):
    res_buffer = buffer_type()
    res_buffer.ParseFromString(data)
    return res_buffer


async def parse_to_object(data, object_class, buffer_type):
    data = MessageToDict(await parse_data(data, buffer_type))
    return object_class(**data)


async def get_file_extension(filename):
    return filename[filename.rfind(".") + 1:]


async def generate_filename(file_ext, prefix="itc_upl_"):
    return f"{prefix}{int(time.time())}{await get_random_string(8)}.{file_ext}"


async def upload_file(file, allowed_extensions, upload_path):
    if file:
        file_ext = await get_file_extension(file.filename)
        if file_ext and file_ext in allowed_extensions:
            contents = file.file.read()
            file_name = await generate_filename(file_ext)
            with open(os.path.join(upload_path, file_name), "wb") as file_descr:
                file_descr.write(contents)
            return {"status": True, "file_name": file_name}
        else:
            return {"status": False, "info": "Files with such extensions are forbidden"}
    else:
        return {"status": False, "info": "no file in request"}
