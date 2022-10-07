import requests
from termcolor import colored
import time
import sys
sys.path.append("../")
import pbs.main_pb2 as MainBuffer


def start_test(tests, url="http://localhost:8080"):
    print(colored(f"Pending tests: {len(tests)}", "green"))
    test_number = 0
    passed_tests = 0
    for test in tests:
        test_status = True
        final_url = f"{url}{test['endpoint']}"
        res = None
        try:
            headers = {"content-type": "application/json"}
            if "serialization_pb" in test and test["serialization_pb"]:
                headers["content-type"] = "application/protobuf"
            if test["method"] == "get":
                res = requests.get(final_url, headers=headers)
            elif test["method"] == "post":
                if "serialization_pb" in test and test["serialization_pb"]:
                    dt = test["buffer_send_name"]()
                    for entry in test["data"]:
                        setattr(dt, entry, test["data"][entry])
                    dt = dt.SerializeToString()
                    res = requests.post(
                        final_url, data=dt, headers=headers)
                else:
                    res = requests.post(
                        final_url, json=test["data"], headers=headers)
        except requests.exceptions.ConnectionError:
            test_status = False

        if res != None and res.status_code == test["code"]:
            try:
                if "serialization_pb" in test and test["serialization_pb"]:
                    data = {}
                    data_buffer = test["buffer_recv_name"]()
                    data_buffer.ParseFromString(res.content)
                    for test_entry in test["res_json"]:
                        data[test_entry] = getattr(data_buffer, test_entry)
                else:
                    data = res.json()
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


if __name__ == "__main__":
    tests = [
        {"endpoint": "/users/1/info", "method": "get", "code": 200,
            "res_json": {"status": True, "first_name": "Stephan", "last_name": "Zhdanov", "github_link": "ret7020"}},
        {"endpoint": "/users/1/info", "method": "get", "code": 200,
            "res_json": {"first_name": "Stephan", "last_name": "Zhdanov", "github_link": "ret7020"}, "serialization_pb": True, "buffer_recv_name": MainBuffer.UserData},
        {"endpoint": "/users/test_auth", "method": "get",
            "code": 403, "res_json": {"detail": "Not authenticated"}},
        {"endpoint": "/auth/login", "method": "post", "code": 200, "res_json": {"token_type": "Bearer"},
            "data": {"email": "ret7020@gmail.com", "password": "12345"}},
        {"endpoint": "/auth/login", "method": "post", "code": 401, "res_json": {},
            "data": {"email": "ret7020@gmail.com", "password": "6262"}},
        {"endpoint": "/auth/login", "method": "post", "code": 200, "res_json": {"token_type": "Bearer"},
         "data": {"email": "ret7020@gmail.com", "password": "12345"}, "serialization_pb": True, "buffer_send_name": MainBuffer.AuthData, "buffer_recv_name": MainBuffer.AccessToken}
    ]
    start_test(tests)
