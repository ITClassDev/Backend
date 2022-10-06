from fastapi import APIRouter, Request, Response
import pbs.test_pb2 as TestBuffer
import asyncio


async def parse_data(data, buffer_type):
    res_buffer = buffer_type()
    res_buffer.ParseFromString(data)
    return res_buffer

async def create_answer(data, buffer_type):
    
    return Response(content=answer_buffer_final, media_type="application/protobuf")

router = APIRouter()


# Dev test
@router.post("/test")
async def test_proto_buffer(request: Request):
    data = await parse_data(await request.body(), TestBuffer.TestData)
    print("Recieve:", data)
    answer_buffer = TestBuffer.TestData()
    answer_buffer.a = 1024
    answer_buffer_final = answer_buffer.SerializeToString()
    print(answer_buffer_final)
    return Response(content=answer_buffer_final, media_type="application/protobuf")