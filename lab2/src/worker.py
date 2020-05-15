import random
import threading
import time
from threading import Thread
import redis

from view import View


class Worker(Thread):

    def __init__(self, delay):
        Thread.__init__(self)
        self.__loop = True
        self.__r = redis.Redis(charset="utf-8", decode_responses=True)
        self.__delay = delay

    def run(self):
        while self.__loop:
            message = self.__r.brpop("queue:")
            if message:
                message_id = int(message[1])

                self.__r.hmset(f"message:{message_id}", {
                    'status': 'checking'
                })
                message = self.__r.hmget(f"message:{message_id}", ["sender_id", "consumer_id"])
                sender_id = int(message[0])
                consumer_id = int(message[1])
                self.__r.hincrby(f"user:{sender_id}", "queue", -1)
                self.__r.hincrby(f"user:{sender_id}", "checking", 1)
                time.sleep(self.__delay)
                is_spam = random.random() > 0.6
                pipeline = self.__r.pipeline(True)
                pipeline.hincrby(f"user:{sender_id}", "checking", -1)
                if is_spam:
                    sender_username = self.__r.hmget(f"user:{sender_id}", 'login')[0]
                    pipeline.zincrby("spam:", 1, f"user:{sender_username}")
                    pipeline.hmset(f"message:{message_id}", {
                        'status': 'blocked'
                    })
                    pipeline.hincrby(f"user:{sender_id}", "blocked", 1)
                    pipeline.publish('spam', f"User {sender_username} sent spam message: \"%s\"" %
                                     self.__r.hmget("message:%s" % message_id, ["text"])[0])
                    print(f"User {sender_username} sent spam message: \"%s\"" % self.__r.hmget("message:%s" % message_id, ["text"])[0])
                else:
                    pipeline.hmset(f"message:{message_id}", {
                        'status': 'sent'
                    })
                    pipeline.hincrby(f"user:{sender_id}", "sent", 1)
                    pipeline.sadd(f"sentto:{consumer_id}", message_id)
                pipeline.execute()

    def stop(self):
        self.__loop = False


if __name__ == '__main__':
    try:
        loop = True
        workers_count = 5
        workers = []
        for x in range(workers_count):
            worker = Worker(random.randint(0, 3))
            worker.setDaemon(True)
            workers.append(worker)
            worker.start()
        while True:
            pass
    except Exception as e:
        View.show_error(str(e))
