import requests
import sys
sys.path.append("../")
import pbs.test_pb2 as TestBuffer

if __name__ == "__main__":
    buffer = TestBuffer.TestData()
    buffer.a = 1024
    buffer_final = buffer.SerializeToString()
    data = requests.post("http://localhost:8080/pb/test", headers={'Content-Type': 'application/protobuf'}, data=buffer_final)
