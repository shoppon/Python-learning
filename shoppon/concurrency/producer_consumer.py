# coding: utf-8
import threading

from datetime import datetime
from time import sleep

MESSAGE_CACHE = []


def log(msg):
    print('[' + str(datetime.now().second) + ']' + msg)


class Producer(threading.Thread):
    def __init__(self, event, message_count=100):
        super(Producer, self).__init__()
        self.producer_event = threading.Event()
        self.producer_event.clear()
        self.consumer_event = event
        self.message_count = message_count
        self.interval = 1
        self.cache = []
        self.complete = False

    def run(self):
        produce_thread = threading.Thread(target=self._produce)
        produce_thread.start()

        send_thread = threading.Thread(target=self._send)
        send_thread.start()

        produce_thread.join()
        send_thread.join()

    def _produce(self):
        count = 1
        while count <= self.message_count:
            log('Produce message--->%s.' % count)
            self.cache.append(count)
            # 通知发送线程已生产
            self.producer_event.set()
            sleep(self.interval)
            count += 1
        self.complete = True

    def _send(self):
        log('Start to send message.')
        while True:
            if len(MESSAGE_CACHE) >= 5:
                # 当消息池满时等待消费者消费
                print('Message cache is full, wait for consuming.')
                self.consumer_event.clear()
                self.consumer_event.wait()
            else:
                while len(MESSAGE_CACHE) < 5:
                    if self.cache:
                        msg = self.cache.pop(0)
                        log('Send message--->%s.' % msg)
                        MESSAGE_CACHE.append(msg)
                        log('Message cache is: %s, cache is: %s after sending '
                            'message.' % (MESSAGE_CACHE, self.cache))
                    else:
                        if self.complete:
                            log('Complete to produce message.')
                            return
                        else:
                            log('No message to send.')
                            # 等待下一个生产者消息
                            self.producer_event.clear()
                            self.producer_event.wait()


class Consumer(threading.Thread):
    def __init__(self, consume_event=None):
        super(Consumer, self).__init__()
        self.consume_event = consume_event
        # 消息间隔2秒
        self.interval = 2
        # 消费消息时间5秒
        self.consume_time = 5
        # 等待10秒无消息则退出
        self.timeout = 10

    def run(self):
        wait = 0
        while True:
            log('Start to consume message.')
            if MESSAGE_CACHE:
                msg = MESSAGE_CACHE.pop(0)
                log('Consume message--->%s.' % msg)
                log('Message cache is: %s after consuming '
                    'message.' % MESSAGE_CACHE)
                sleep(self.consume_time)
                wait = 0
                # 通知生产者生产
                self.consume_event.set()
            else:
                log('Message cache is empty, just wait.')
                if wait >= self.timeout:
                    log('Wait %s no message, exit.' % self.timeout)
                    break
                else:
                    sleep(self.interval)
                    wait += self.interval


def main():
    event = threading.Event()
    producer = Producer(event)
    producer.start()

    for _ in range(2):
        Consumer(event).start()

    producer.join()


if __name__ == '__main__':
    main()
