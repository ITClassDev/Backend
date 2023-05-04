import gzip
from typing import Callable, List

from fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute
import uvicorn
from pydantic import BaseModel
import test_pb2 as proto_defines
from google.protobuf.json_format import MessageToJson
from protobuf_to_dict import protobuf_to_dict
import json
from starlette.concurrency import iterate_in_threadpool
from google.protobuf import json_format

class SumIn(BaseModel):
    a: int
    b: int

class RequestSwitcher(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "serialization" in self.headers and self.headers["serialization"] == "proto3":
                buffer_name = self.url.path.replace("/", "_")[1:] # buffer name 
                print("Proto:", buffer_name)
                input_buffer = getattr(proto_defines, f"{buffer_name}_in")
                input_buffer = input_buffer.FromString(body)
                body = json.dumps(protobuf_to_dict(input_buffer)).encode("utf-8")
            self._body = body
        return self._body


class Proto3RouteOverlay(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()
        async def custom_route_handler(request: Request) -> Response:
            print("Overlay triggered")
            request = RequestSwitcher(request.scope, request.receive)
            response = await original_route_handler(request)
            print(response.content)
            return response

        return custom_route_handler


app = FastAPI()
app.router.route_class = Proto3RouteOverlay
'''
@app.middleware("http")
async def process_serialization(request: Request, call_next):
    if "serialization" in request.headers and request.headers["serialization"] == "proto3": # switch to protobuf mode
        buffer_name = request.url.path.replace("/", "_")[1:] # output buffer
        response = await call_next(request)
        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        response_json = response_body[0].decode()
        
        answer_buffer = getattr(proto_defines, buffer_name)()
        answer_buffer = json_format.Parse(response_json, answer_buffer)
        answer_buffer = answer_buffer.SerializeToString()
        return Response(content=answer_buffer, status_code=response.status_code, media_type="application/proto3")
    else: # keep json mode
        #print(await request.body())
        return await call_next(request)

'''
@app.post("/sum")
async def sum_numbers(nums: SumIn):
    return {"sum": nums.a + nums.b}



if __name__ == "__main__":
    uvicorn.run("custom_route:app", port=8080, reload=True)

