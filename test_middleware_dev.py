from fastapi import FastAPI, Request, Response
import uvicorn
from starlette.concurrency import iterate_in_threadpool
import json
import test_pb2 as proto_defines
from google.protobuf import json_format
from protobuf_to_dict import protobuf_to_dict
from pydantic import BaseModel

from starlette.datastructures import Headers
#from starlette.requests import Request as ReqBase

app = FastAPI(title="Test Proto REST auto switch")

class SumIn(BaseModel):
    a: int
    b: int

def build_request(
    scope: dict,
    body: str = None,
) -> Request:

    request = Request(scope)
    if body:
        async def request_body():
            return body
        request.body = request_body
    return request

@app.middleware("http")
async def process_serialization(request: Request, call_next): 
    if "Content-Type" in request.headers and request.headers["Content-Type"] == "application/proto3": # swith to protobuf mode
        buffer_name = request.url.path.replace("/", "_")[1:] # output buffer
        request_data = await request.body() 
        if request_data:
            input_buffer = getattr(proto_defines, f"{buffer_name}_in")
            input_buffer = input_buffer.FromString(request_data)
            #print(type(input_buffer.a))
            #print(protobuf_to_dict(input_buffer))
            #print(protobuf_to_dict(input_buffer))
            print(request.scope)
            request = build_request(request.scope, body=b'{\n  "a": 0,\n  "b": 0\n}')
            print(await request.body())
        response = await call_next(request)
        
        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        response_json = response_body[0].decode()
        print(response_json)
        answer_buffer = getattr(proto_defines, buffer_name)()
        answer_buffer = json_format.Parse(response_json, answer_buffer)
        answer_buffer = answer_buffer.SerializeToString()
        return Response(content=answer_buffer, status_code=response.status_code, media_type="application/proto3")
    else: # keep json mode
        print(await request.body())
        return await call_next(request)

@app.get("/get_json")
async def get_json():
    return {"test": "asd", "res": "sdf"}

@app.get("/multi/layer/children/struct")
async def multi_layer():
    return {"test": "1231", "res": "sfsdf"}

@app.post("/sum")
async def sum_(sum_in: SumIn):
    return {"sum": sum_in.a + sum_in.b}

if __name__ == "__main__":
    uvicorn.run("app:app", port=8080, reload=True)
