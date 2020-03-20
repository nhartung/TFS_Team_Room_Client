import requests
from requests_ntlm import HttpNtlmAuth

def get_session(username, password):
    session = requests.Session()
    session.auth = HttpNtlmAuth(f'ACA\\{username}', password)
    return session

def get_available_rooms(session, url):
    REST_PATH = '/_apis/chat/rooms'
    headers = {'user-agent' : 'TFS-Team-Room-Client',
               'Accept'     : 'application/json;odata=verbose'}
    response = session.get(url + REST_PATH, headers = headers)
    data = response.json()
    rooms = []
    if( data['count'] > 0 ):
        rooms = data['value']
    return rooms

def get_room_messages(session, url, room_id):
    REST_PATH = f'/_apis/chat/rooms/{room_id}/messages'
    headers = {'user-agent' : 'TFS-Team-Room-Client',
               'Accept'     : 'application/json;odata=verbose'}
    response = session.get(url + REST_PATH, headers = headers)
    data = response.json()
    messages = []
    if( data['count'] > 0 ):
        messages = data['value']
    return messages
