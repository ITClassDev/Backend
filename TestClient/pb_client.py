import requests
import sys
sys.path.append("../")
import pbs.main_pb2 as MainBuffer

def parse_data(data, buffer_type):
    res_buffer = buffer_type()
    res_buffer.ParseFromString(data)
    return res_buffer



if __name__ == "__main__":
    '''buffer = MainBuffer.User()
    buffer.a = 1024
    buffer_final = buffer.SerializeToString()'''
    data = requests.get("http://localhost:8080/users/1/info", headers={'Content-Type': 'application/protobuf'})
    answer = data.content
    parsed = parse_data(answer, MainBuffer.UserData)
    print("Answer:", parsed.first_name)
