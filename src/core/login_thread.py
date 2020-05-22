from threading import Thread 
from queue import Empty

from back_end.tfs_rest import (
    get_available_rooms,
    get_session,
    TFS_Chat_Exception
)

BASE_URL = 'http://hv-tfs:8080/tfs/Engineering Organization/'
class Login_Thread(Thread):
    def __init__(
            self, 
            event, 
            login_success_callback, 
            login_failure_callback,
            login_queue,
    ):
        Thread.__init__(self)
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
