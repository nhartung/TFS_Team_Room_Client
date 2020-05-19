from queue import Queue, Empty

from kivy.core.window import Window

from kivy.lang.builder import Builder

from kivy.uix.screenmanager import Screen

Builder.load_file('src/gui/login_screen.kv')

class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__()
        self.username = None
        self.password = None
        self.queue = None
        Window.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        ENTER_KEY = 40
        if keycode == ENTER_KEY:
            self._login()

    def _login(self):
        self.queue.put((self.f_username.text, self.f_password.text))

    def set_login_queue(self, queue):
        self.queue = queue
