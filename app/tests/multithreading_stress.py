from multiprocessing import Process
import requests
import time


class Stresser:
    def __init__(self, url="http://localhost:8080"):
        self.url = url

    def stress_thread(self, endpoint, each_thread, headers={}):
        time_sum = 0
        for req_num in range(each_thread):
            start_req_time = time.time()
            req = requests.get(f"{self.url}{endpoint}", headers=headers)
            time_took = time.time() - start_req_time
            time_sum += time_took
        print("Avg time per req:", time_sum / each_thread)

    def m_threaded_wrapper(self, endpoint, each_thread, threads_cnt, headers):
        for _ in range(threads_cnt):
            Process(target=lambda: self.stress_thread(endpoint, each_thread, headers)).start()


if __name__ == "__main__":
    stress = Stresser()
    stress.m_threaded_wrapper("/auth/me", 100, 100, headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyZXQ3MDIwQGdtYWlsLmNvbSIsImV4cCI6MTY3MjA4NDc4N30.QO9oTmGbyn8lnmePI_9-aoGI4S-Qu4QyaguL-BekYXc"})
