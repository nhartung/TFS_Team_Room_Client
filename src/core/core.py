from threading import Thread, Event

from back_end.tfs_rest import (
    TFS_Chat_Exception,
    Connection_Error,
    Invalid_Response,
    get_session,
    get_available_rooms,
    get_room_messages
)

from core.room import Room

BASE_URL = 'http://hv-tfs:8080/tfs/Engineering Organization/'
class Core(Thread):
    def __init__(self, callback_obj):
        Thread.__init__(self)
        self.callback_obj = callback_obj
        self.stopped = Event()
        self.login_event = Event()
        self.login_thread = Login_Thread(
            self.login_event, 
            self.callback_obj.login_function, 
            self.callback_obj.login_ready_function, 
            self._login_success, 
            self._login_failure)
        self.get_rooms_event = Event()
        self.session = None
        
    def run(self):
        self.login_thread.start()

        while not self.login_event.wait(1):
            pass

        self.get_rooms_thread = Get_Rooms_Thread(
            self.get_rooms_event, 
            self.session, 
            self.callback_obj.rooms_callback)
        self.get_rooms_thread.start()
        while not self.stopped.wait(1):
            pass

    def _login_success(self):
        self.session = self.login_thread.session
        self.callback_obj.login_success_callback()
        self.login_event.set()

    def _login_failure(self, reason):
        self.callback_obj.login_failure_callback(reason)

    def stop(self):
        self.login_event.set()
        self.get_rooms_event.set()
        self.login_thread.join()
        self.get_rooms_thread.join()
        self.stopped.set()

class Login_Thread(Thread):
    def __init__(
            self, 
            event, 
            login_func, 
            login_ready_func, 
            login_success_callback, 
            login_failure_callback
    ):
        Thread.__init__(self)
        self.login_func = login_func
        self.login_ready_func = login_ready_func
        self.login_success_callback = login_success_callback
        self.login_failure_callback = login_failure_callback
        self.stopped = event
        self.session = None
        self.logged_in = False

    def run(self):
        username = None
        password = None
        while not self.logged_in:
            while not self.stopped.wait(1) and not self.login_ready_func():
                pass
            if self.stopped.isSet():
                break
            if self.login_ready_func():
                username, password = self.login_func()
                self.session = get_session(username, password)
                try:
                    get_available_rooms(self.session, BASE_URL)
                    self.login_success_callback()
                    self.logged_in = True
                    self.stopped.set()
                except TFS_Chat_Exception:
                    username = None
                    password = None
                    self.login_failure_callback("Login failed.")

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
