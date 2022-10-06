from fastapi import APIRouter, Request
import pbs.test_pb2 as TestBuffer
import asyncio




router = APIRouter()
@router.post("/test")
async def test_proto_buffer(request: Request):
    data = await request.body()
    res_buffer = TestBuffer.TestData()
    print(data)
    res_buffer.ParseFromString(data)
    print(res_buffer.a)

