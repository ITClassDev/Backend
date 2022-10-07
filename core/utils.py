from fastapi import Request, Response
import json
from google.protobuf import json_format

NON_AUTH_PACKET = {"status": False, "info": "Non authed"}


async def create_answer(data: dict, buffer_type, return_object=False):
    answer_buffer = buffer_type()
    for el in data:
        if el != "status":  # REST API JSON REQ STATUS
            setattr(answer_buffer, el, data[el])
    if return_object:
        return answer_buffer
    answer_buffer_final = answer_buffer.SerializeToString()
    return Response(content=answer_buffer_final, media_type="application/protobuf")

# Depr
async def create_answer_from_dict(data: dict, buffer_type):
    print(data)
    answer_buffer = buffer_type()
    json_string = json.dumps(data)
    return json_format.Parse(json_string, answer_buffer)


async def check_req_type(req: Request):
    req_type = "applciation/json"
    if "content-type" in req.headers:
        req_type = req.headers["content-type"]
    return req_type

async def parse_data(data, buffer_type):
    res_buffer = buffer_type()
    res_buffer.ParseFromString(data)
    return res_buffer
