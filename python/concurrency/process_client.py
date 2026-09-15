from array import array
from multiprocessing.connection import Client

address = ("localhost", 6000)


def main():
    with Client(address, authkey=b"secret password") as client:
        print(client.recv())
        print(client.recv_bytes())
        arr = array("i", [0, 0, 0, 0, 0])
        client.recv_bytes_into(arr)
        print(arr)


if __name__ == '__main__':
    main()
