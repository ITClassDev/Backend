import requests
from termcolor import colored
import time
import sys
sys.path.append("../")
import pbs.main_pb2 as MainBuffer

from google.protobuf.json_format import MessageToDict



def start_test(tests, url="http://localhost:8080"):
    print(colored(f"Pending tests: {len(tests)}", "green"))
    test_number = 0
    passed_tests = 0
    for test in tests:
        test_status = True
        final_url = f"{url}{test['endpoint']}"
        res = None
        try:
            if test["method"] == "get":
                res = requests.get(final_url)
            elif test["method"] == "post":
                if "serialization_pb" in test and test["serialization_pb"]:
                    dt = test["buffer_send_name"]()
                    for entry in test["data"]:
                        setattr(dt, entry, test["data"][entry])
                    dt = dt.SerializeToString()
                    res = requests.post(
                        final_url, data=dt)
                else:
                    res = requests.post(
                        final_url, json=test["data"])
        except requests.exceptions.ConnectionError:
            test_status = False
        if res != None and res.status_code == test["code"]:
            try:
                if "serialization_pb" in test and test["serialization_pb"]:
                    if "buffer_recv_name" in test:
                        data_buffer = test["buffer_recv_name"]()
                        data_buffer.ParseFromString(res.content)
                        data = MessageToDict(data_buffer)
                        if "key_to_extract" in test:
                            data = data[test["key_to_extract"]]
                    else:
                        data = {}
                    
                else:
                    data = res.json()
                if "element_ind" in test:
                    data = data[test["element_ind"]]
                for test_attr in test["res_json"]:
                    if not (test_attr in data and test["res_json"][test_attr] == data[test_attr]):
                        test_status = False
            except requests.exceptions.JSONDecodeError:
                test_status = False
        else:
            test_status = False

        test_status_text = "OK" if test_status else "FAIL"
        test_status_color = "green" if test_status else "red"
        print(
            f"Test #{test_number} - {colored(test_status_text, test_status_color)}")
        if test_status:
            passed_tests += 1
        test_number += 1
    print(colored(
        f"Tests passed {passed_tests}/{len(tests)} - {(passed_tests / len(tests) * 100)}%", "yellow"))
    return len(tests), passed_tests


if __name__ == "__main__":
    tests_for_json = [
        {"endpoint": "/users/1/info", "method": "get", "code": 200,
            "res_json": {"status": True, "firstName": "Stephan", "lastName": "Zhdanov", "githubLink": "ret7020"}},
        {"endpoint": "/users/10/info", "method": "get", "code": 200,
            "res_json": {"status": False}},
        {"endpoint": "/users/test_auth", "method": "get",
            "code": 403, "res_json": {"detail": "Not authenticated"}},
        {"endpoint": "/auth/login", "method": "post", "code": 200, "res_json": {"tokenType": "Bearer"},
            "data": {"email": "ret7020@gmail.com", "password": "12345"}},
        {"endpoint": "/auth/login", "method": "post", "code": 401, "res_json": {},
            "data": {"email": "ret7020@gmail.com", "password": "6262"}},
    ]
    print("Testing JSON")
    json_all, json_passed = start_test(tests_for_json)
    print("Testing protobuf")
    tests_for_protobuf = [
        {"endpoint": "/users/1/info", "method": "get", "code": 200, 
            "res_json": {"status": True, "firstName": "Stephan", "lastName": "Zhdanov", "githubLink": "ret7020"}, "serialization_pb": True, "buffer_recv_name": MainBuffer.UserData},
        {"endpoint": "/users/10/info", "method": "get", "code": 200, 
            "res_json": {"status": False}, "serialization_pb": True, "buffer_recv_name": MainBuffer.UserData},
        {"endpoint": "/auth/login", "method": "post", "code": 200, 
            "data": {"email": "ret7020@gmail.com", "password": "12345"}, "res_json": {"tokenType": "Bearer"}, "serialization_pb": True, "buffer_recv_name": MainBuffer.AccessToken, "buffer_send_name": MainBuffer.AuthData},
        {"endpoint": "/auth/login", "method": "post", "code": 401, 
            "data": {"email": "ret7020@gmail.com", "password": "ahfhsdhf"}, "res_json": {}, "serialization_pb": True, "buffer_send_name": MainBuffer.AuthData},
        
    ]
    protobuf_all, protobuf_passed = start_test(tests_for_protobuf, url="http://localhost:8080/mobile")
    print(colored(f"Summary: passed {json_passed + protobuf_passed}/{json_all + protobuf_all}", color="red"))
