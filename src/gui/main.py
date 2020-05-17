from core.core import Core

from gui.chat_window import ChatWindowScreen
from gui.login_screen import LoginScreen

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

from threading import Thread

sm = ScreenManager()
login_screen = LoginScreen(name='login')
login_screen.set_sm(sm)
sm.add_widget(login_screen)
chat_screen = ChatWindowScreen(name='chat_window')
sm.add_widget(chat_screen)


class TFS_ChatApp(App):
    def build(self):
        Window.size = (1280,720)
        return sm

class GUI_Manager():
    def __init__(self):
        self.messages_queue = None

    def rooms_callback(self, rooms):
        chat_screen.set_rooms(rooms)

    def users_callback(self, users):
        chat_screen.set_users(users)

    def get_room_function(self):
        return chat_screen.get_room_id()

    def messages_callback(self, messages):
        chat_screen.set_messages(messages)

    def login_ready_function(self):
        return login_screen.entry_ready

    def login_function(self):
        return (login_screen.username, login_screen.password)

    def login_success_callback(self):
        sm.current = 'chat_window'

    def login_failure_callback(self, reason):
        print("Reason: " + reason)
        login_screen.entry_ready = False

    def set_message_queue(self, queue):
        chat_screen.set_message_queue(queue)

def main():
    manager = GUI_Manager()
    core = Core(manager)
    core.start()
    TFS_ChatApp().run()
    core.stop()
    core.join()
