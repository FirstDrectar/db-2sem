import redis
import datetime
import logging

logging.basicConfig(filename="./events.log", level=logging.INFO)


class RedisServer(object):
    def __init__(self):
        self.__r = redis.Redis(charset="utf-8", decode_responses=True)

    def registration(self, username):
        if self.__r.hget('users:', username):
            raise Exception(f"User with name: \'{username}\' already exists")

        user_id = self.__r.incr('user:id:')
        pipeline = self.__r.pipeline(True)
        pipeline.hset('users:', username, user_id)
        pipeline.hmset(f"user:{user_id}", {
            'login': username,
            'id': user_id,
            'queue': 0,
            'checking': 0,
            'blocked': 0,
            'sent': 0,
            'delivered': 0
        })

        pipeline.execute()
        logging.info(f"User {username} registered at {datetime.datetime.now()} \n")
        return user_id

    def sign_in(self, username):
        user_id = self.__r.hget("users:", username)

        if not user_id:
            raise Exception(f"User {username} does not exist ")

        self.__r.sadd("online:", username)
        logging.info(f"User {username} logged in at {datetime.datetime.now()} \n")
        self.__r.publish('users', "User %s signed in" % self.__r.hmget(f"user:{user_id}", 'login')[0])
        return int(user_id)

    def sign_out(self, user_id) -> int:
        logging.info(f"User {user_id} signed out at {datetime.datetime.now()} \n")
        self.__r.publish('users', "User %s signed out" % self.__r.hmget(f"user:{user_id}", 'login')[0])
        return self.__r.srem("online:", self.__r.hmget(f"user:{user_id}", 'login')[0])

    def create_message(self, message_text, consumer, sender_id) -> int:

        message_id = int(self.__r.incr('message:id:'))
        consumer_id = self.__r.hget("users:", consumer)

        if not consumer_id:
            raise Exception(f"{consumer} user does not exist, user can't send a message")

        pipeline = self.__r.pipeline(True)

        pipeline.hmset('message:%s' % message_id, {
            'text': message_text,
            'id': message_id,
            'sender_id': sender_id,
            'consumer_id': consumer_id,
            'status': "created"
        })
        pipeline.lpush("queue:", message_id)
        pipeline.hmset('message:%s' % message_id, {
            'status': 'queue'
        })
        pipeline.zincrby("sent:", 1, "user:%s" % self.__r.hmget(f"user:{sender_id}", 'login')[0])
        pipeline.hincrby(f"user:{sender_id}", "queue", 1)
        pipeline.execute()

        return message_id

    def get_messages(self, user_id):
        messages = self.__r.smembers(f"sentto:{user_id}")
        messages_list = []
        for message_id in messages:
            message = self.__r.hmget(f"message:{message_id}", ["sender_id", "text", "status"])
            sender_id = message[0]
            messages_list.append("From: %s - %s" % (self.__r.hmget("user:%s" % sender_id, 'login')[0], message[1]))
            if message[2] != "delivered":
                pipeline = self.__r.pipeline(True)
                pipeline.hset(f"message:{message_id}", "status", "delivered")
                pipeline.hincrby(f"user:{sender_id}", "sent", -1)
                pipeline.hincrby(f"user:{sender_id}", "delivered", 1)
                pipeline.execute()
        return messages_list

    def get_message_statistics(self, user_id):
        current_user = self.__r.hmget(f"user:{user_id}", ['queue', 'checking', 'blocked', 'sent', 'delivered'])
        return "In queue: %s\nChecking: %s\nBlocked: %s\nSent: %s\nDelivered: %s" % tuple(current_user)

    def get_online_users(self) -> list:
        return self.__r.smembers("online:")

    def get_top_senders(self, amount_of_top_senders) -> list:
        return self.__r.zrange("sent:", 0, int(amount_of_top_senders) - 1, desc=True, withscores=True)

    def get_top_spamers(self, amount_of_top_spamers) -> list:
        return self.__r.zrange("spam:", 0, int(amount_of_top_spamers) - 1, desc=True, withscores=True)

