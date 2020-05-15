from controller.UserController import UserController
from controller.AdminController import AdminController
from controller.Controller import Controller

menu_list = {
    'Main menu': {
        'Registration': UserController.registration,
        'Sign in': UserController.sign_in,
        'Exit': Controller.stop_loop,
    },
    'Utilizer menu': {
        'Sign out': UserController.sign_out,
        'Send a message': UserController.send_message,
        'Inbox messages': UserController.inbox_message,
        'My messages statistics': UserController.get_message_statistics,
    },
    'Admin menu': {
        'Sign out': Controller.stop_loop,
        'Get events': AdminController.get_events,
        'Online users': AdminController.get_online_users,
        'Top senders': AdminController.get_top_senders,
        'Top spamers': AdminController.get_top_spamers,
    }
}

roles = {
    'utilizer': 'Utilizer menu',
    'admin': 'Admin menu'
}

special_parameters = {
    'role': '(admin or utilizer)'
}
