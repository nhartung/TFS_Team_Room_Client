from threading import Thread

from back_end.tfs_rest import (
    get_available_rooms
)

from core.config_reader import get_base_url
from core.room import Room

class Get_Rooms_Thread(Thread):
    def __init__(self, event, session, callback_func):
        Thread.__init__(self)
        self.stopped = event
        self.session = session
        self.callback_func = callback_func
        self.rooms = []
        self.last_response = None

    def run(self):
        first = True
        # TODO, replace time with a configurable option.
        while first or not self.stopped.wait(10):
            first = False
            response = get_available_rooms(self.session, get_base_url())
            if self.last_response != response:
                self.last_response = response
                self.rooms = self._build_rooms(self.last_response)
                self.callback_func(self.rooms)

    def _build_rooms(self, response):
        d = {}
        for entry in response:
            # TODO: Need to confirm if all of the required keys exist
            room = Room(entry['name'], entry['description'], entry['lastActivity'])
            d[entry['id']] = room
        return d
