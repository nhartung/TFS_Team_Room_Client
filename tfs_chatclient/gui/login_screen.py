from queue import Queue, Empty

from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen

import os

from tfs_chatclient.core.config_reader import get_domain

KV_FILE = os.path.join(os.path.dirname(__file__), 'login_screen.kv')
Builder.load_file(KV_FILE)
class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__()
        self.username = None
        self.password = None
        self.queue = None
        domain = get_domain()
        if domain:
            self.f_user_label.text += ' ' + domain + '\\'
        Window.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        ENTER_KEY = 40
        if keycode == ENTER_KEY:
            self._login()

    def _login(self):
        self.queue.put((self.f_username.text, self.f_password.text))

    def set_login_queue(self, queue):
        self.queue = queue
