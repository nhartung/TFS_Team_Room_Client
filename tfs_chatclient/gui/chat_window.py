from kivy.factory import Factory

from kivy.lang.builder import Builder

from kivy.event import EventDispatcher
from kivy.graphics import Color
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty, ListProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.screenmanager import Screen

import os
import re

KV_FILE = os.path.join(os.path.dirname(__file__), 'chat_window.kv')
Builder.load_file(KV_FILE)

# There's probably a more elegant way than using a global variable here.
selected_room_id = None

class SelectableRecycleBoxLayout(LayoutSelectionBehavior, RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    selected_value = StringProperty('')

class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            global selected_room_id
            selected_room_id = rv.data[index]['room_id']

class UserLabel(Label, EventDispatcher):
    lcolor = ListProperty([0.5, 0.5, 0.5, 1])

class RoomListRV(RecycleView):
    rv_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RoomListRV, self).__init__(**kwargs)
        self.data = [{}]

class UserListRV(RecycleView):
    rv_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(UserListRV, self).__init__(**kwargs)
        self.data = [{}]

class ChatLabel(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        if 'username' in data and 'text' in data and 'timestamp' in data:
            self.cl_username.text = data['username']
            self.cl_text.text = data['text']
            self.cl_timestamp.text = self._get_timestamp(data['timestamp'])
            return super(ChatLabel, self).refresh_view_attrs(rv, index, data)

    def _get_timestamp(self, string):
        match = re.search('.*T(.*)\..*', string)
        if match:
            return match.group(1)
        else:
            return 'Unknown Time'


class EntryWidget(BoxLayout):
    def _send_message(self):
        if self.message_queue:
            self.message_queue.put(self.ew_text.text)
        self.ew_text.text = ""

    def set_message_queue(self, queue):
        self.message_queue = queue


class MessageListRV(RecycleView):
    rv_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MessageListRV, self).__init__(**kwargs)
        self.data = [{}]

class ChatWindowScreen(Screen):
    def __init__(self, **kwargs):
        super(ChatWindowScreen, self).__init__(**kwargs)
        self.entry_widget = EntryWidget()
        self.room_list_rv = RoomListRV()
        self.user_list_rv = UserListRV()
        self.message_list_rv = MessageListRV()
        self.f_chat_rooms.add_widget(self.room_list_rv)
        self.f_chat_room_content.add_widget(self.message_list_rv)
        self.f_chat_room_content.add_widget(self.entry_widget)
        self.f_chat_room_users.add_widget(self.user_list_rv)

    def set_rooms(self, rooms):
        self.room_list_rv.data = [{'text': rooms[room_id].name, 'room_id': room_id} for room_id in sorted(rooms)]

    def set_users(self, users):
        temp_list = []
        for user in users:
            d = {}
            d['text'] = user['user']['displayName']
            if user['isOnline']:
                d['lcolor'] = [0.0, 1.0, 0.0, 1.0]
            else:
                d['lcolor'] = [0.5, 0.5, 0.5, 1.0]
            temp_list.append(d)
        self.user_list_rv.data = temp_list

    def set_message_queue(self, queue):
        self.entry_widget.set_message_queue(queue)

    def get_room_id(self):
        global selected_room_id
        return selected_room_id

    def set_messages(self, messages):
        # TODO: Try to find a more efficient method than rebuilding this list
        # every time a new message is detected.
        temp_list = []
        for message in messages:
            temp_list.append(
                {
                   'username' : message['postedBy']['displayName'],
                   'text' : message['content'],
                   'timestamp' : message['postedTime']
                }
            )
        self.message_list_rv.data = temp_list
