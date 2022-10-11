import requests
import time
import threading

class Stresser:

    def __init__(self, url="http://localhost:8080"):
        self.url = url

    def stress_thread(self, endpoint, each_thread):
        time_sum = 0
        for req_num in range(each_thread):
           start_req_time = time.time()
           req = requests.get(f"{self.url}{endpoint}") 
           time_took = time.time() - start_req_time
           time_sum += time_took
        print("Avg time per req:", time_sum / each_thread)
    
    def m_threaded_wrapper(self, endpoint, each_thread, threads_cnt):
        for _ in range(threads_cnt):
            threading.Thread(target= lambda: self.stress_thread(endpoint, each_thread)).start()


if __name__ == "__main__":
    stress = Stresser()
    stress.m_threaded_wrapper("/users/1/info", 100, 100)
