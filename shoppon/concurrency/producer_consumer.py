import threading

from datetime import datetime
from time import sleep

MESSAGE_CACHE = []


def log(msg):
    print('[' + str(datetime.now().second) + ']' + msg)


class Producer(threading.Thread):
    def __init__(self, condition, message_count=10):
        super(Producer, self).__init__()
        self.condition = condition
        self.message_count = message_count
        self.interval = 1
        self.cache = []
        self.complete = False

    def run(self):
        log('Start to produce message.')

        produce_thread = threading.Thread(target=self._produce)
        produce_thread.start()

        send_thread = threading.Thread(target=self._send)
        send_thread.start()

        produce_thread.join()
        send_thread.join()

    def _produce(self):
        count = 1
        self.condition.acquire()
        while count <= self.message_count:
            log('Produce message--->%s.' % count)
            self.cache.append(count)
            self.condition.notifyAll()
            self.condition.wait()
            sleep(self.interval)
            count += 1
        self.complete = True
        self.condition.release()

    def _send(self):
        log('Start to send message.')
        self.condition.acquire()
        while True:
            if len(MESSAGE_CACHE) >= 5:
                self.condition.notifyAll()
                self.condition.wait()
            else:
                if self.cache:
                    msg = self.cache.pop(0)
                    log('Send message--->%s.' % msg)
                    MESSAGE_CACHE.append(msg)
                    log('Message cache is: %s after sending '
                        'message.' % MESSAGE_CACHE)
                    self.condition.notifyAll()
                    self.condition.wait()
                else:
                    if self.complete:
                        log('Complete to produce message.')
                        break
                    else:
                        log('No message to send.')
                        self.condition.notifyAll()
                        self.condition.wait()


class Consumer(threading.Thread):
    def __init__(self, condition=None):
        super(Consumer, self).__init__()
        self.condition = condition
        self.interval = 5

    def run(self):
        log('Start to consume message.')
        self.condition.acquire()
        while True:
            if MESSAGE_CACHE:
                msg = MESSAGE_CACHE.pop(0)
                log('Consume message--->%s.' % msg)
                log('Message cache is: %s after consuming '
                    'message.' % MESSAGE_CACHE)
                self.condition.notifyAll()
                self.condition.wait()
                sleep(self.interval)
            else:
                log('Message cache is empty, just wait.')
                try:
                    self.condition.notifyAll()
                    self.condition.wait(10)
                except:
                    log('Timeout!')
                    self.condition.release()
                    break


def main():
    lock = threading.RLock()
    condition = threading.Condition(lock=lock)
    producer = Producer(condition)
    producer.start()

    for _ in range(2):
        Consumer(condition).start()

    producer.join()


if __name__ == '__main__':
    main()
