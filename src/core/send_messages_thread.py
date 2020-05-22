from threading import Thread
from queue import Empty

from back_end.tfs_rest import (
    send_message
)

from core.config_reader import get_base_url

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
                send_message(self.session, get_base_url(), self.get_room_func(), message)
                self.queue.task_done()
            except Empty:
                # This exception is part of the normal flow is the user has not
                # sent a message in the last timeout period. Simply passing.
                pass
