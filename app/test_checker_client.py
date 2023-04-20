import socket
import json

payload = {"source_code": "print(int(input()) + int(input()))", "language": 0, "tests": [
    {"input": "1\n2", "output": "3"}], "submit_id": 666, "type": 0}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 7778))
sock.send(json.dumps(payload).encode("utf-8"))
sock.close()