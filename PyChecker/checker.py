import epicbox
import sys
import argparse
import json
import time
from typing import List
import asyncio

class Checker:
    def __init__(self):
        # Setup epicbox
        epicbox.configure(
            profiles=[
                epicbox.Profile('python', 'stepik/epicbox-python:3.10.6'),
                epicbox.Profile('g++', 'stepik/epicbox-gcc:10.2.1')
            ]
        )
        self.tasks_queue = []

    def get_tasks_stat(self):
        tasks_active = 0
        task_pending = 0
   
    def check_one_task_thread(self, test_code, tests, env, callback, submit_id, loop) -> None:
        files = [{'name': 'main.py', 'content': test_code}]
        limits = {'cputime': env["cpu_time_limit"], 'memory': env["memory_limit"], 'realtime': env["real_time_limit"]}
        tests_statuses = []
        tests_passed = 0
        for test in tests:
            result = epicbox.run('python', 'python3 main.py', files=files, limits=limits, stdin=test["input"])
            test_status = result["stdout"].decode("utf-8").strip() == test["output"]
            tests_passed += test_status
            tests_statuses.append({"status": test_status, "error_info": result["stderr"], "duration": result["duration"], "timeout": result["timeout"], "memoryout": result["oom_killed"]})
        print("Checker finished")
        callback((tests_passed == len(tests), tests_statuses, submit_id), loop)


    def check_multiple_tasks(self):
        pass
def process_checker_result(res):
    print("Checker result:", res)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check task cli')
    parser.add_argument('--source_code', type=str,
                    help='Path to test file')
    parser.add_argument('--tests', type=str,
                    help='Path to tests json file')
    args = parser.parse_args()
    with open(args.source_code, "rb") as test_code_fd:
        test_code = test_code_fd.read()

    with open(args.tests) as test_fd:
        tests = json.load(test_fd)

    checker = Checker()
    checker.check_one_task(test_code, tests, process_checker_result)
    while True:
        print("Polling checker statistic")
        time.sleep(1)
