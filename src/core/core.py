from threading import Thread, Event

from back_end.tfs_rest import (
    get_session,
    get_available_rooms,
    get_room_messages
)

from core.room import Room

BASE_URL = 'http://hv-tfs:8080/tfs/Engineering Organization/'
class Core():
    def __init__(self, username, password, callback_obj):
        self.session = get_session(username, password)
        self.callback_obj = callback_obj
        self.get_rooms_event = Event()
        self.get_rooms_thread = Get_Rooms_Thread(self.get_rooms_event, self.session, self.callback_obj.rooms_callback)
        self.get_rooms_thread.start()

    def stop(self):
       self.get_rooms_event.set()


class Get_Rooms_Thread(Thread):
    def __init__(self, event, session, callback_func):
        Thread.__init__(self)
        self.stopped = event
        self.session = session
        self.callback_func = callback_func
        self.rooms = []
        self.last_response = None

    def run(self):
        # TODO, replace time with a configurable option.
        while not self.stopped.wait(10):
            response = get_available_rooms(self.session, BASE_URL)
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
