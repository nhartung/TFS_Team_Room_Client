from threading import Thread, Event
from queue import Queue

from core.get_rooms_thread import Get_Rooms_Thread
from core.login_thread import Login_Thread
from core.send_messages_thread import Send_Messages_Thread
from core.room_data_thread import Room_Data_Thread

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
            self.callback_obj.room_provider_callback)
        self.get_rooms_thread.start()

        self.get_messages_thread = Room_Data_Thread(
            self.get_messages_event,
            self.session,
            self.callback_obj.get_selected_room,
            self.callback_obj.message_provider_callback,
            self.callback_obj.user_provider_callback)
        self.get_messages_thread.start()

        self.send_messages_thread = Send_Messages_Thread(
            self.send_messages_event,
            self.session,
            self.messages_queue,
            self.callback_obj.get_selected_room)
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
