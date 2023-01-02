import sys
sys.path.append("../../")
import pbs.main_pb2 as MainBuffer
import requests


def parse_data(data, buffer_type):
    res_buffer = buffer_type()
    res_buffer.ParseFromString(data)
    return res_buffer


if __name__ == "__main__":
    buffer = MainBuffer.AuthData()
    buffer.email = "ret7020@gmail.com"
    buffer.password = "12345"
    buffer_final = buffer.SerializeToString()
    data = requests.post("http://localhost:8080/mobile/auth/login/", data=buffer_final)
    answer = data.content
    parsed = parse_data(answer, MainBuffer.AccessToken)
    access_token = parsed.accessToken
    print(f"Token: {access_token}")
    #data = requests.post("http://localhost:8080/auth")
