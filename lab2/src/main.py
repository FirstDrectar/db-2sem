from controller.AdminController import AdminController
from controller.Controller import Controller
from controller.UserController import UserController
from controller.EmulationController import EmulationController
from worker import Worker
from view import View
from faker import Faker
import random
import time


def emulation():
    fake = Faker()
    users_count = 5
    users = [fake.profile(fields=['username'], sex=None)['username'] for u in range(users_count)]
    threads = []
    try:

        for i in range(users_count):
            threads.append(EmulationController(users[i], users, users_count, random.randint(100, 5000)))
        for thread in threads:
            thread.start()

        AdminController()

        for thread in threads:
            if thread.is_alive():
                thread.stop()
    except Exception as e:
        View.show_error(str(e))


if __name__ == "__main__":

    choice = Controller.make_choice(["Main", "Emulation"], "Program mode")
    if choice == 0:
        UserController()
    elif choice == 1:
        emulation()
