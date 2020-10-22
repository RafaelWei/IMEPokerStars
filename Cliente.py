import socket 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 8080
host = '127.0.0.2'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.send(b"Hello World!")
    data = s.recv(1024)

    print("Received: ", data)