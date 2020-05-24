import datetime
from threading import Thread
from queue import Empty

from tfs_chatclient.back_end.tfs_rest import (
    TFS_Chat_Exception,
    get_my_user_id,
    get_room_messages,
    get_room_info,
    get_users,
    join_room,
    leave_room
)

from tfs_chatclient.core.config_reader import get_base_url

class Room_Data_Thread(Thread):
    def __init__(self, event, session, get_room_func, messages_callback, users_callback):
        Thread.__init__(self)
        self.stopped = event
        self.session = session
        self.get_room_func = get_room_func
        self.messages_callback = messages_callback
        self.users_callback = users_callback
        self.last_room_update = datetime.date(1970, 1, 1)
        self.room_id = None

    def run(self):
        while not self.stopped.wait(1):
            last_room_id = self.room_id
            self.room_id = self.get_room_func()
            if self.room_id is not None:
                if last_room_id == self.room_id:
                    self._get_updated_text()
                else:
                    # New Room
                    user_id = get_my_user_id(self.session, get_base_url())
                    if last_room_id is not None:
                        self._leave_room(last_room_id, user_id)
                    self._join_room(user_id)
                    self._get_room_text()
            else:
                # Do nothing when a room isn't selected
                pass

    def _get_updated_text(self):
        last_update_time = self._get_last_update_time()
        if self.last_room_update != last_update_time:
            self.last_room_update = last_update_time
            messages = get_room_messages(self.session, get_base_url(), self.room_id)
            self.messages_callback(messages)

    def _get_room_text(self):
        last_update_time = self._get_last_update_time()
        self.last_room_update = last_update_time
        messages = get_room_messages(self.session, get_base_url(), self.room_id)
        self.messages_callback(messages)
        users = get_users(self.session, get_base_url(), self.room_id)
        self.users_callback(users)

    def _get_last_update_time(self):
        latest_update = get_room_info(self.session, get_base_url(), self.room_id)['lastActivity']
        last_update_time = (
            datetime.datetime.strptime(latest_update,'%Y-%m-%dT%H:%M:%S.%fZ'))
        return last_update_time
    
    def _join_room(self, user_id):
        try:
            join_room(self.session, get_base_url(), self.room_id, user_id)
        except TFS_Chat_Exception:
            print("Failed to join room!")

    def _leave_room(self, room_id, user_id):
        try:
            leave_room(self.session, get_base_url(), room_id, user_id)
        except TFS_Chat_Exception:
            print("Failed to leave room!")
