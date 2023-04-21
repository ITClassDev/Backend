# import socket
# import json
# from PyChecker.checker import Checker
# import multiprocessing
# import os

# checker = Checker()

# HOST = "localhost"
# PORT = 7777

# # Simple PoC
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))
# s.listen()
# conn, addr = s.accept()

# def callback(data):
#     print(data)
#     conn.send(json.dumps(data).encode("utf-8"))

# with conn:
#     print(f"Connected by {addr}")
#     while True:
#         #print("Listening loop")
#         data = conn.recv(1000)
#         if data:
#             data = json.loads(data)
#             print(data)
#             if data["type"] == 0: # Single task
#                 # Static limits
#                 env = {"cpu_time_limit": 2, "memory_limit": 1024, "real_time_limit": 2}
#                 path = os.path.join("/home/stephan/Progs/ItClassDevelopment/Backend/app/static/users_data/uploads/tasks_source_codes", data["source_code_path"])
#                 checker_listen_process = multiprocessing.Process(target=lambda: checker.check_one_task_thread(path, data["language"], data["tests"], env, callback, data["submit_id"], 1))
#                 checker_listen_process.start()

#             elif data["type"] == 1: # Contest
#                 pass
#         else:
#             print("Client leave")
#             conn.close()
#             break
        
import fastapi
import uvicorn

