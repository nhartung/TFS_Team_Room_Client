from getpass import getpass
import json
import requests
from requests_ntlm import HttpNtlmAuth

from back_end.tfs_rest import (
    get_session,
    get_available_rooms,
    get_room_messages
)

def main():
    BASE_URL = 'http://hv-tfs:8080/tfs/Engineering Organization/'
    username = input('Username: ACA\\')
    password = getpass()

    session = get_session(username, password)
    rooms = get_available_rooms(session, BASE_URL)
    print('Hello TFS Rooms.')
    for room in rooms:
        print(str(room['id']) + ': ' + room['name'])

    messages = get_room_messages(session, BASE_URL, 34)
    print('Hello TFS Messages.')
    for message in messages:
        print(str(message['postedBy']['displayName']) + ': ' + message['content'])
