import requests
from requests_ntlm import HttpNtlmAuth
import sys

class TFS_Chat_Exception(Exception):
    pass

class HTTP_Request_Exception(TFS_Chat_Exception):
    pass

class Connection_Error(HTTP_Request_Exception):
    pass

class Invalid_Response(HTTP_Request_Exception):
    pass

def _get_request(session, url):
    data = None
    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.ConnectionError:
        print('Unable to establish a connection.', file=sys.stderr)
        raise Connection_Error()
    except requests.exceptions.HTTPError as e:
        print('Invalid HTTP Response: ' + str(e), file=sys.stderr)
        raise Invalid_Response()
    except Exception as e:
        print('An unknown error has occured: ' + str(type(e)) + ': ' + str(e), file=sys.stderr)
        raise TFS_Chat_Exception()
    return data

def get_session(username, password):
    session = None
    session = requests.Session()
    session.auth = HttpNtlmAuth(f'ACA\\{username}', password)
    headers = {'user-agent' : 'TFS-Team-Room-Client',
               'Accept'     : 'application/json;odata=verbose'}
    session.headers.update(headers)
    return session

def get_available_rooms(session, url):
    REST_PATH = '/_apis/chat/rooms'
    rooms = []
    data = _get_request(session, url + REST_PATH, )
    if( data and data['count'] > 0 ):
        rooms = data['value']
    return rooms

def get_room_messages(session, url, room_id):
    REST_PATH = f'/_apis/chat/rooms/{room_id}/messages'
    messages = []
    data = _get_request(session, url + REST_PATH)
    if( data and data['count'] > 0 ):
        messages = data['value']
    return messages
