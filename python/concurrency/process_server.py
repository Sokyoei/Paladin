from array import array
from multiprocessing.connection import Listener

address = ("localhost", 6000)


def main():
    with Listener(address, authkey=b"secret password") as listener, listener.accept() as server:
        print(listener.last_accepted)
        server.send([2.25, None, "Ahri"])
        server.send_bytes(b"Sokyoei")
        server.send_bytes(array("i", [1, 2, 3, 4, 5]))


if __name__ == '__main__':
    main()
