from fastapi import FastAPI, Request, Response
import uvicorn
from starlette.concurrency import iterate_in_threadpool
import json
import test_pb2 as proto_defines
from google.protobuf import json_format

app = FastAPI(title="Test Proto REST")


@app.middleware("http")
async def process_serialization(request: Request, call_next):
    data_type = request.headers["accept"]
    buffer_name = request.url.path.replace("/", "_")[1:]
    print(buffer_name) 
    if data_type == "application/json":
        response = await call_next(request) # hardcode for now
        return response
    elif data_type == "application/proto3":
        response = await call_next(request) # hardcode for now
        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        response_json = response_body[0].decode()
        answer_buffer = getattr(proto_defines, buffer_name)()
        answer_buffer = json_format.Parse(response_json, answer_buffer)
        answer_buffer = answer_buffer.SerializeToString()
        return Response(content=answer_buffer, status_code=response.status_code, media_type="application/protobuf")

@app.get("/get_json")
async def get_json():
    return {"test": "asd", "res": "sdf"}

@app.get("/multi/layer/children/struct")
async def multi_layer():
    return {"test": "1231", "res": "sfsdf"}

if __name__ == "__main__":
    uvicorn.run("app:app", port=8080, reload=True)
