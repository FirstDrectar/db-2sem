class View(object):

    @staticmethod
    def draw_menu(menu_list, name_of_menu: str):
        print(f"\n{name_of_menu}")
        number = 0
        for menu_item in menu_list:
            print(f" {number}: {menu_item}")
            number += 1

    @staticmethod
    def show_item(item):
        print(f"Item: {item}")

    @staticmethod
    def show_items(items: list):
        count = 1
        for item in items:
            print(f"{count}: {item}")
            count += 1

    @staticmethod
    def show_error(err: str):
        print(f"Error: {err}")

    @staticmethod
    def show_text(text: str):
        print(text)

    @staticmethod
    def print_line():
        print('-----------------------------------------------------------------------------------------')

    @staticmethod
    def print_list(name_of_list, list):
        print(name_of_list)
        count = 1
        for item in list:
            print(f"{count}: {item}")
            count += 1
