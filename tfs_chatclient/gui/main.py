from core.core import Core
from core.app_manager import App_Manager

from gui.chat_window import ChatWindowScreen
from gui.login_screen import LoginScreen

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

from threading import Thread

sm = ScreenManager()
login_screen = LoginScreen(name='login')
sm.add_widget(login_screen)
chat_screen = ChatWindowScreen(name='chat_window')
sm.add_widget(chat_screen)


class TFS_ChatApp(App):
    def build(self):
        Window.size = (1280,720)
        return sm

class GUI_Manager(App_Manager):
    def __init__(self):
        self.messages_queue = None

    def room_provider_callback(self, rooms):
        chat_screen.set_rooms(rooms)

    def user_provider_callback(self, users):
        chat_screen.set_users(users)

    def message_provider_callback(self, messages):
        chat_screen.set_messages(messages)

    def login_success_callback(self):
        sm.current = 'chat_window'

    def login_failure_callback(self, reason):
        print("Reason: " + reason)
        login_screen.entry_ready = False

    def get_selected_room(self):
        return chat_screen.get_room_id()

    def set_message_queue(self, queue):
        chat_screen.set_message_queue(queue)

    def set_login_queue(self, queue):
        login_screen.set_login_queue(queue)

def main():
    manager = GUI_Manager()
    core = Core(manager)
    core.start()
    TFS_ChatApp().run()
    core.stop()
    core.join()
