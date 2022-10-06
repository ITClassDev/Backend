import requests
from termcolor import colored
import time

def start_test(tests, url="http://localhost:8080"):
    print(colored(f"Pending tests: {len(tests)}", "green"))
    test_status = True
    test_number = 0
    passed_tests = 0
    for test in tests:
        final_url = f"{url}{test['endpoint']}"
        if test["method"] == "get":
            res = requests.get(final_url)
        elif test["method"] == "post":
            res = requests.post(final_url)

        if res.status_code == test["code"]:
            try:
                data = res.json()
                for test_attr in test["res_json"]:
                    if not(test_attr in test["res_json"] and test["res_json"][test_attr] == data[test_attr]):
                        test_status = False
            except requests.exceptions.JSONDecodeError:
                test_status = False
        else:
            test_status = False 
        
        test_status_text = "OK"  if test_status else "FAIL"
        test_status_color = "green" if test_status else "red"
        print(f"Test #{test_number} - {colored(test_status_text, test_status_color)}")
        if test_status: passed_tests += 1
        test_number += 1
    print(colored(f"Tests passed {passed_tests}/{len(tests)} - {(passed_tests / len(tests) * 100)}%", "yellow"))

       


if __name__ == "__main__":
    tests = [
        {"endpoint": "/users/1/info", "method": "get", "code": 200, "res_json": {"status": True, "first_name": "Stephan", "last_name": "Zhdanov"}},
        {"endpoint": "/users/test_auth", "method": "get", "code": 403, "res_json": {"detail": "Not authenticated"}}
    ]
    start_test(tests)