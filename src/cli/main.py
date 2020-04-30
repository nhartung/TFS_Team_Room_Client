from getpass import getpass
import json
import msvcrt
import requests
from requests_ntlm import HttpNtlmAuth

from core.core import Core

class CLI_Manager():
    def __init__(self):
        self.rooms = []
        pass

    def rooms_callback(self, rooms):
        self.rooms = rooms
        self._update_room_list()

    def _update_room_list(self):
        self.room_window.clear()
        y = 0
        for key in self.rooms:
            self.room_window.addstr(y, 0, self.rooms[key].name)
            y += 1
        self.room_window.refresh()

def main():
    username = input('Username: ACA\\')
    password = getpass()

    print("TODO!")
    return
    #  core = Core(CLI_Manager())

    # Debug code for now, ensuring that we can kill the multi-threaded app.
    while True:
        if msvcrt.kbhit():
            key = ord( msvcrt.getch() )
            if(key == ord('k')):
                print('Killing application...')
                core.stop()
                break
    #  messages = get_room_messages(session, BASE_URL, 34)
    #  print('Hello TFS Messages.')
    #  for message in messages:
        #  print(str(message['postedBy']['displayName']) + ': ' + message['content'])
