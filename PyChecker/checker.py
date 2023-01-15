import epicbox
import sys
import argparse
import json
import time
import os
from typing import List
import asyncio
import string
import random
import shutil

class Checker:
    def __init__(self):
        # Setup epicbox
        epicbox.configure(
            profiles={
                epicbox.Profile('python', 'stepik/epicbox-python:3.10.6'),
                epicbox.Profile('gcc', 'stepik/epicbox-gcc:10.2.1'),
            }
        )
        self.tasks_queue = []
        self.temp_workspace = "/home/stephan/Progs/ItClassDevelopment/Backend/PyChecker/tmp/"

    def name_gen(self, length=10):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str;

    def get_tasks_stat(self):
        tasks_active = 0
        task_pending = 0

    def check_one_task_thread(self, test_code, source_file_name, tests, env, callback, submit_id, loop) -> None:
        # MESSY HACKATHON
        # FIXIT
        limits = {'cputime': env["cpu_time_limit"], 'memory': env["memory_limit"], 'realtime': env["real_time_limit"]}
        language = {"py": 0, "cpp": 1}[source_file_name.split(".")[-1]]
        if language == 0:  # python
            files = [{'name': 'main.py', 'content': test_code}]
            tests_statuses = []
            tests_passed = 0
            for test in tests:
                result = epicbox.run('python', 'python3 main.py', files=files, limits=limits, stdin=test["input"])
                test_status = result["stdout"].decode("utf-8").strip() == test["output"]
                tests_passed += test_status
                tests_statuses.append \
                    ({"status": test_status, "error_info": result["stderr"], "duration": result["duration"],
                      "timeout": result["timeout"], "memoryout": result["oom_killed"]})
            # print("Checker finished")
            callback((tests_passed == len(tests), tests_statuses, submit_id), loop)
        elif language == 1:  # c++
            # like session storage
            with epicbox.working_directory() as workdir:
                # compile
                compile_res = epicbox.run('gcc', 'g++ -pipe -O2 -static -o main main.cpp',
                                          files=[{'name': 'main.cpp', 'content': test_code}],
                                          workdir=workdir,
                                          limits={'cputime': 10, 'memory': 2048, 'realtime': 10})  # static build limits
                if compile_res['exit_code'] == 0:
                    tests_statuses = []
                    tests_passed = 0
                    # iterate over tests
                    for test in tests:
                        result = epicbox.run('gcc', './main', stdin=test["input"],
                                             limits=limits,
                                             workdir=workdir)
                        test_status = result["stdout"].decode("utf-8").strip() == test["output"]
                        tests_passed += test_status
                        tests_statuses.append \
                            ({"status": test_status, "error_info": result["stderr"], "duration": result["duration"],
                              "timeout": result["timeout"], "memoryout": result["oom_killed"]})
                    callback((tests_passed == len(tests), tests_statuses, submit_id),
                             loop)  # send result data, to callback
                else:
                    callback((False, [], submit_id), loop)

    def fetch_git(self, git_path):
        fetch_path = os.path.join(self.temp_workspace, self.name_gen())
        os.system(f"git clone {git_path} {fetch_path}")
        return fetch_path

    def check_multiple_tasks(self, git_path, tests, env, callback, submit_id, loop):
        source_path = self.fetch_git(git_path)
        with open(os.path.join(source_path, "header.h"), "rb") as header_fd:
            header_code = header_fd.read()
        with open(os.path.join(source_path, "funcs.cpp"), "rb") as funcs_fd:
            funcs_code = funcs_fd.read()
            for test_func in tests:
                test_func_statuses = []
                base = '#include <iostream>\n#include <string.h>\n#include "header.h"\nint main(){\n'
                arg_counter = 0
                for arg in range(len(list(test_func.values())[0][0]["input"])):
                    arg_type = {str: "string", int: "int"}[type(list(test_func.values())[0][0]["input"][arg])]
                    base += f"{arg_type} a{arg};\n    std::cin >> a{arg};\n    "
                    arg_counter += 1

                main_code = base + f"std::cout << {list(test_func.keys())[0]}(" 
                for i in range(arg_counter-1):
                    main_code += f"a{i},"
                main_code += f"a{arg_counter-1});\n"
                main_code += "}"
                with epicbox.working_directory() as workdir:
                    files = [{'name': 'main.cpp', 'content': main_code.encode("utf-8")}, {'name': 'header.h', 'content': header_code}, {'name': 'funcs.cpp', 'content': funcs_code}]
                    compile_res = epicbox.run('gcc', 'g++ -pipe -O2 -static -o main main.cpp funcs.cpp',
                                        files=files,
                                        workdir=workdir,
                                        limits={'cputime': 10, 'memory': 2048, 'realtime': 10})  # static build limits
                    if compile_res['exit_code'] == 0:
                        tests_statuses = []
                        tests_passed = 0

                        # iterate over tests
                        test_set = list(test_func.values())[0]
                        for test in test_set:
                            #print("\n".join(test["input"]))
                            stdin_ = '\n'.join(str(x) for x in test["input"]).encode("utf-8")
                            result = epicbox.run('gcc', './main', stdin=stdin_,
                                                limits=env,
                                                workdir=workdir)
                            print(result)
                            test_status = result["stdout"].decode("utf-8").strip() == str(test["output"])
                            tests_passed += test_status
                            tests_statuses.append({"status": test_status, "error_info": result["stderr"]})
                        test_func_statuses.append(tests_statuses)

                        callback((tests_passed == len(test_set), tests_statuses, submit_id),
                            loop)  # send result data, to callback
                    else:
                        callback((False, [], submit_id), loop)
        shutil.rmtree(source_path)

if __name__ == "__main__":
    checker = Checker()
    tests = [
        {"sum": [
            {"input": [100, 120], "output": "220"},
            {"input": [20, 43], "output": 63},
            {"input": [7, 123], "output": 130}
        ]},
        {"concat": [
            {"input": ["a", "b"], "output": "ab"},
            {"input": ["Hello", ",world!"], "output": "Hello,world!"},
            {"input": ["Result", "string"], "output": "Resultstring"}
        ]}
    ]
    checker.check_multiple_tasks("https://github.com/ITClassDev/TestSolutions/", tests, {'cputime': 2, 'memory': 200, 'realtime': 200}, lambda x, y: print(x), 100, None)
    #print(checker.name_gen())
    # parser = argparse.ArgumentParser(description='Check task cli')
    # parser.add_argument('--source_code', type=str, help='Path to test file')
    # parser.add_argument('--tests', type=str, help='Path to tests json file')
    # args = parser.parse_args()
    # # LEGACY
    # with open(args.source_code, "rb") as test_code_fd:
    #     test_code = test_code_fd.read()

    # with open(args.tests) as test_fd:
    #     tests = json.load(test_fd)

    # # LEGACY
    # checker = Checker()
    # checker.check_one_task_thread(test_code, tests, process_checker_result)
    # while True:
    #     print("Polling checker statistic")
    #     time.sleep(1)
