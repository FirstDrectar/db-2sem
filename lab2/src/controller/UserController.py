from inspect import signature
import atexit
from controller.Controller import Controller

from view import View
from redis_server.RedisServer import RedisServer


class UserController(object):
    def __init__(self):
        self.__server = RedisServer()
        self.__menu = 'Main menu'
        self.__current_user_id = -1
        self.loop = True
        atexit.register(self.sign_out)
        self.start()

    def start(self):
        from data import menu_list
        try:
            while self.loop:
                choice = Controller.make_choice(menu_list[self.__menu].keys(), self.__menu)
                Controller.considering_choice(self, choice, list(menu_list[self.__menu].values()))

        except Exception as e:
            View.show_error(str(e))

    def registration(self):
        self.__server.registration(*Controller.get_func_arguments(self.__server.registration))

    def sign_in(self):
        user_id = self.__server.sign_in(*Controller.get_func_arguments(self.__server.sign_in))
        self.__current_user_id = user_id

        self.__menu = 'Utilizer menu'

    def sign_out(self):
        if self.__current_user_id != -1:
            self.__server.sign_out(self.__current_user_id)
            self.__menu = 'Main menu'
            self.__current_user_id = -1

    def send_message(self):
        self.__server.create_message(*Controller.get_func_arguments(self.__server.create_message, 1),
                                           self.__current_user_id)

    def inbox_message(self):
        messages = self.__server.get_messages(self.__current_user_id)
        View.print_list("Messages:", messages)

    def get_message_statistics(self):
        statistics = self.__server.get_message_statistics(self.__current_user_id)
        View.show_item(statistics)

