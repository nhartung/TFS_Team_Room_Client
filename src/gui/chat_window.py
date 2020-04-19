from kivy.factory import Factory

from kivy.lang.builder import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

Builder.load_file('src/gui/chat_window.kv')

class ChatWindowScreen(Screen):
    def _set_sm(self, sm):
        self.sm = sm

    def set_rooms(self, rooms):
        for room_id in rooms:
            room = rooms[room_id]
            self.f_chat_rooms.add_widget(Label(text=room.name))
        self.f_chat_rooms.add_widget(BoxLayout())
