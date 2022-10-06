from fastapi import APIRouter, Request, Response
import pbs.test_pb2 as TestBuffer
import asyncio


async def parse_data(data, buffer_type):
    res_buffer = buffer_type()
    res_buffer.ParseFromString(data)
    return res_buffer

async def create_answer(data: dict, buffer_type):
    answer_buffer = buffer_type()
    for el in data:
        setattr(answer_buffer, el, data[el])
    answer_buffer_final = answer_buffer.SerializeToString()
    return Response(content=answer_buffer_final, media_type="application/protobuf")

router = APIRouter()


# Dev test route
@router.post("/test")
async def test_proto_buffer(request: Request):
    data = await parse_data(await request.body(), TestBuffer.TestData)
    print("Recieve:", data)
    return await create_answer({"a": 1024}, TestBuffer.TestData)