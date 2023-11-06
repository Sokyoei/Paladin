import threading


def do_work():
    print(123)


threading.Thread(do_work())
