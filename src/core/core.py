import datetime
from threading import Thread, Event
from queue import Queue, Empty

from back_end.tfs_rest import (
    TFS_Chat_Exception,
    Connection_Error,
    Invalid_Response,
    get_session,
    get_available_rooms,
    get_room_info,
    get_room_messages,
    get_my_user_id,
    get_users,
    join_room,
    leave_room,
    send_message
)

from core.room import Room

BASE_URL = 'http://hv-tfs:8080/tfs/Engineering Organization/'
class Core(Thread):
    def __init__(self, callback_obj):
        Thread.__init__(self)
        self.callback_obj = callback_obj
        self.stopped = Event()

        self.login_queue = Queue()
        callback_obj.set_login_queue(self.login_queue)
        self.login_event = Event()
        self.login_thread = Login_Thread(
            self.login_event, 
            self.callback_obj.login_function, 
            self.callback_obj.login_ready_function, 
            self._login_success, 
            self._login_failure,
            self.login_queue)

        self.get_rooms_thread = None
        self.get_messages_thread = None
        self.get_rooms_event = Event()
        self.get_messages_event = Event()
        self.send_messages_event = Event()
        self.session = None

        self.messages_queue = Queue()
        callback_obj.set_message_queue(self.messages_queue)
        
    def _login_success(self):
        self.session = self.login_thread.session
        self.callback_obj.login_success_callback()
        self.login_event.set()

    def _login_failure(self, reason):
        self.callback_obj.login_failure_callback(reason)

    def run(self):
        self._login()

        if not self.stopped.isSet():
            self._start_chat_threads()

        self._wait_for_app_end()

    def _login(self):
        self.login_thread.start()
        self._wait_for_login()

    def _wait_for_login(self):
        while not self.login_event.wait(1):
            pass

    def _start_chat_threads(self):
        self.get_rooms_thread = Get_Rooms_Thread(
            self.get_rooms_event, 
            self.session, 
            self.callback_obj.rooms_callback)
        self.get_rooms_thread.start()

        self.get_messages_thread = Get_Messages_Thread(
            self.get_messages_event,
            self.session,
            self.callback_obj.get_room_function,
            self.callback_obj.messages_callback,
            self.callback_obj.users_callback)
        self.get_messages_thread.start()

        self.send_messages_thread = Send_Messages_Thread(
            self.send_messages_event,
            self.session,
            self.messages_queue,
            self.callback_obj.get_room_function)
        self.send_messages_thread.start()

    def _wait_for_app_end(self):
        while not self.stopped.wait(1):
            pass

    def stop(self):
        self.login_event.set()
        self.get_rooms_event.set()
        self.get_messages_event.set()
        self.send_messages_event.set()
        if self.login_thread and self.login_thread.is_alive():
            self.login_thread.join()
        if self.get_rooms_thread and self.get_rooms_thread.is_alive():
            self.get_rooms_thread.join()
        if self.get_messages_thread and self.get_messages_thread.is_alive():
            self.get_messages_thread.join()
        if self.send_messages_thread and self.send_messages_thread.is_alive():
            self.send_messages_thread.join()
        self.stopped.set()

class Login_Thread(Thread):
    def __init__(
            self, 
            event, 
            login_func, 
            login_ready_func, 
            login_success_callback, 
            login_failure_callback,
            login_queue,
    ):
        Thread.__init__(self)
        self.login_func = login_func
        self.login_ready_func = login_ready_func
        self.login_success_callback = login_success_callback
        self.login_failure_callback = login_failure_callback
        self.queue = login_queue
        self.stopped = event
        self.session = None

    def run(self):
        username = None
        password = None
        while not self.stopped.wait(0.1):
            try:
                username, password = self.queue.get(block=True, timeout=1)
                self.session = get_session(username, password)
                self.queue.task_done()
                get_available_rooms(self.session, BASE_URL)
                self.login_success_callback()
                self.stopped.set()
            except Empty:
                # This exception is part of the normal flow is the user has not
                # sent a message in the last timeout period. Simply passing.
                pass
            except TFS_Chat_Exception:
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

class Get_Messages_Thread(Thread):
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
                    user_id = get_my_user_id(self.session, BASE_URL)
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
            messages = get_room_messages(self.session, BASE_URL, self.room_id)
            self.messages_callback(messages)

    def _get_room_text(self):
        last_update_time = self._get_last_update_time()
        self.last_room_update = last_update_time
        messages = get_room_messages(self.session, BASE_URL, self.room_id)
        self.messages_callback(messages)
        users = get_users(self.session, BASE_URL, self.room_id)
        self.users_callback(users)

    def _get_last_update_time(self):
        latest_update = get_room_info(self.session, BASE_URL, self.room_id)['lastActivity']
        last_update_time = (
            datetime.datetime.strptime(latest_update,'%Y-%m-%dT%H:%M:%S.%fZ'))
        return last_update_time
    
    def _join_room(self, user_id):
        try:
            join_room(self.session, BASE_URL, self.room_id, user_id)
        except TFS_Chat_Exception:
            print("Failed to join room!")

    def _leave_room(self, room_id, user_id):
        try:
            leave_room(self.session, BASE_URL, room_id, user_id)
        except TFS_Chat_Exception:
            print("Failed to leave room!")

class Send_Messages_Thread(Thread):
    def __init__(self, event, session, queue, get_room_func):
        Thread.__init__(self)
        self.get_room_func = get_room_func
        self.stopped = event
        self.session = session
        self.queue = queue

    def run(self):
        while not self.stopped.wait(0.1):
            try:
                message = self.queue.get(block=True, timeout=1)
                send_message(self.session, BASE_URL, self.get_room_func(), message)
                self.queue.task_done()
            except Empty:
                # This exception is part of the normal flow is the user has not
                # sent a message in the last timeout period. Simply passing.
                pass
