import socket
import time

HOST = "localhost"
PORT = 7778

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            conn.sendall(b"Hello, yept")
            time.sleep(5)
            
