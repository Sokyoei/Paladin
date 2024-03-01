import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()  # 获取本地主机名
port = 8888
s.bind((host, port))
# s.setblocking(True)
s.listen(5)  # 等待客户端连接
while True:
    c, address = s.accept()
    print(f"link address: {address}")
    data = input("please input something:")
    if data == "quit":
        break
    c.send(data.encode())
c.close()
