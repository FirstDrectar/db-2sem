from controller.Controller import Controller
from listener.Listener import EventListener
from redis_server.RedisServer import RedisServer
import atexit

from view import View


class AdminController(object):
    def __init__(self):
        self.__server = RedisServer()
        self.loop = True
        self.__listener = EventListener()
        self.__listener.start()
        self.start()

    def start(self):
        from data import menu_list
        try:
            menu = "Admin menu"
            while self.loop:
                choice = Controller.make_choice(menu_list[menu].keys(), menu)
                Controller.considering_choice(self, choice, list(menu_list[menu].values()))
        except Exception as e:
            View.show_error(str(e))

    def get_events(self):
        events = self.__listener.get_events()
        View.print_list("Events: ", events)

    def get_online_users(self):
        online_users = self.__server.get_online_users()
        View.print_list("Online users: ", online_users)

    def get_top_senders(self):
        top_senders = self.__server.get_top_senders(
            *Controller.get_func_arguments(self.__server.get_top_senders))
        View.print_list("Top senders: ", top_senders)

    def get_top_spamers(self):
        top_spamers = self.__server.get_top_spamers(
            *Controller.get_func_arguments(self.__server.get_top_spamers))
        View.print_list("Top spamers: ", top_spamers)