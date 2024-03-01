import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
print(host)
port = 8888

s.connect((host, port))
while True:
    a = s.recv(1024)
    if a:
        print(s.recv(1024).decode())
    if a.decode() == "quit":
        break
s.close()
