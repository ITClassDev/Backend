import requests
import sys
sys.path.append("../")
import pbs.main_pb2 as MainBuffer

def parse_data(data, buffer_type):
    res_buffer = buffer_type()
    res_buffer.ParseFromString(data)
    return res_buffer



if __name__ == "__main__":
    buffer = MainBuffer.AuthData()
    buffer.email = "ret7020@gmail.com"
    buffer.password = "12345"
    buffer_final = buffer.SerializeToString()
    data = requests.post("http://localhost:8080/auth/login/", headers={'Content-Type': 'application/protobuf'}, data=buffer_final)
    answer = data.content
    parsed = parse_data(answer, MainBuffer.AccessToken)
    print("Answer:", parsed)
