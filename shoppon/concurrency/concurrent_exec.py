import threading

import time

num = 0


def add():
    global num
    num += 1


def wait(event):
    count = 0
    while count < 5:
        print('Start')
        event.wait()
        event.clear()
        count += 1
        print('End')


def main():
    ths = []
    for _ in range(10):
        th = threading.Thread(target=add)
        ths.append(th)

    for th in ths:
        th.start()


def send_event():
    ev = threading.Event()
    th = threading.Thread(target=wait, args=(ev,))
    th.start()
    time.sleep(5)
    ev.set()


if __name__ == '__main__':
    send_event()
