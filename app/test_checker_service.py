import socket
import json
from PyChecker.checker import Checker
import multiprocessing

checker = Checker()

HOST = "localhost"
PORT = 7778

# Simple PoC
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()
callback = lambda x: print("Verdict:", x)

with conn:
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024)
        if data:
            data = json.loads(data)
            print(data)
            if data["type"] == 0: # Single task
                # Static limits
                env = {"cpu_time_limit": 2, "memory_limit": 1024, "real_time_limit": 2}
                checker_listen_process = multiprocessing.Process(target=lambda: checker.check_one_task_thread(data["source_code"], data["language"], data["tests"], env, callback, data["submit_id"], 1))
                checker_listen_process.start()
                
            elif data["type"] == 1: # Contest
                pass
        
