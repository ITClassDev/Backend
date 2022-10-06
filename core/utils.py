from fastapi import Request, Response

NON_AUTH_PACKET = {"status": False, "info": "Non authed"}


async def create_answer(data: dict, buffer_type):
    answer_buffer = buffer_type()
    for el in data:
        if el != "status":  # REST API JSON REQ STATUS
            setattr(answer_buffer, el, data[el])
    answer_buffer_final = answer_buffer.SerializeToString()
    return Response(content=answer_buffer_final, media_type="application/protobuf")


async def check_req_type(req: Request):
    req_type = "applciation/json"
    if "content-type" in req.headers:
        req_type = req.headers["content-type"]
    return req_type

async def parse_data(data, buffer_type):
    res_buffer = buffer_type()
    res_buffer.ParseFromString(data)
    return res_buffer
