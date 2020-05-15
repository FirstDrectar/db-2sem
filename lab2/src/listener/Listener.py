import datetime
from threading import Thread
import logging

import redis


class EventListener(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__r = redis.Redis(charset="utf-8", decode_responses=True)
        self.__events = []

    def run(self):
        pubsub = self.__r.pubsub()
        pubsub.subscribe(['users', 'spam'])
        for item in pubsub.listen():
            if item['type'] == 'message':
                message = "\nEVENT: %s | %s" % (item['data'], datetime.datetime.now())
                self.__events.append(message)
                logging.info(message)

    def get_events(self):
        return self.__events
