from time import sleep
from threading import Event
from threading import Thread


class Worker:
    def __init__(self, event):
        self.event = event

    def run(self):
        while not self.event.is_set():
            sleep(1)
            print("I'm working!")


class Controller:
    def __init__(self, event):
        self.event = event

    def run(self):
        input()
        self.event.set()


if __name__ == "__main__":
    event = Event()
    worker = Worker(event)
    controller = Controller(event)
    Thread(target=worker.run).start()
    Thread(target=controller.run).start()
