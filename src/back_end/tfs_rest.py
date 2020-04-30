import json
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

def _put_request(session, url, data = {}, params = {}, headers = {}):
    try:
        response = session.put(url, data=json.dumps(data), params=params, headers=headers)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print('Unable to establish a connection.', file=sys.stderr)
        raise Connection_Error()
    except requests.exceptions.HTTPError as e:
        print('Invalid HTTP Response: ' + str(e), file=sys.stderr)
        raise Invalid_Response()
    except Exception as e:
        print('An unknown error has occured: ' + str(type(e)) + ': ' + str(e), file=sys.stderr)
        raise TFS_Chat_Exception()

def _post_request(session, url, data = {}, params = {}, headers = {}):
    try:
        response = session.post(url, data=json.dumps(data), params=params, headers=headers)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print('Unable to establish a connection.', file=sys.stderr)
        raise Connection_Error()
    except requests.exceptions.HTTPError as e:
        print('Invalid HTTP Response: ' + str(e), file=sys.stderr)
        raise Invalid_Response()
    except Exception as e:
        print('An unknown error has occured: ' + str(type(e)) + ': ' + str(e), file=sys.stderr)
        raise TFS_Chat_Exception()

def _delete_request(session, url, data = {}, params = {}, headers = {}):
    try:
        response = session.delete(url, data=json.dumps(data), params=params, headers=headers)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print('Unable to establish a connection.', file=sys.stderr)
        raise Connection_Error()
    except requests.exceptions.HTTPError as e:
        print('Invalid HTTP Response: ' + str(e), file=sys.stderr)
        raise Invalid_Response()
    except Exception as e:
        print('An unknown error has occured: ' + str(type(e)) + ': ' + str(e), file=sys.stderr)
        raise TFS_Chat_Exception()

def get_session(username, password):
    session = None
    session = requests.Session()
    session.auth = HttpNtlmAuth(f'ACA\\{username}', password)
    headers = {'user-agent'   : 'TFS-Team-Room-Client',
               'Accept'       : 'application/json;odata=verbose',
               'content-type' : 'application/json',
               'api-version'  : '1.0'}
    session.headers.update(headers)
    return session

def get_available_rooms(session, url):
    REST_PATH = '/_apis/chat/rooms'
    rooms = []
    data = _get_request(session, url + REST_PATH, )
    if( data and data['count'] > 0 ):
        rooms = data['value']
    #  response = [{'id' : 1, 'name' : 'Test Room', 'description' : 'LOL', 'lastActivity' : 'WHO CARES'}]
    return rooms

def get_room_info(session, url, room_id):
    REST_PATH = f'/_apis/chat/rooms/{room_id}'
    #  mock_data = {'id': 1, 'name': '412 Retrofit Team Room', 'description': '', 'lastActivity': '2020-04-23T20:48:55.583Z', 'createdBy': {'id': '9cb92aa1-e840-4214-8bcc-33e8054cbc54', 'displayName': '[Engineering Organization]\\Project Collection Service Accounts', 'url': 'http://hv-tfs:8080/tfs/Engineering Organization/_apis/Identities/9cb92aa1-e840-4214-8bcc-33e8054cbc54', 'imageUrl': 'http://hv-tfs:8080/tfs/Engineering Organization/_api/_common/identityImage?id=9cb92aa1-e840-4214-8bcc-33e8054cbc54'}, 'createdDate': '2020-01-08T16:16:17.68Z', 'hasAdminPermissions': True, 'hasReadWritePermissions': True}
    room_info = _get_request(session, url + REST_PATH)
    return room_info

def get_room_messages(session, url, room_id):
    REST_PATH = f'/_apis/chat/rooms/{room_id}/messages'
    messages = []
    data = _get_request(session, url + REST_PATH)
    if( data and data['count'] > 0 ):
        messages = data['value']
    #  mock_messages = [{'id': 1100, 'content': 'Hello, this is a asdf;lkajsdf;kljasdf;kljasdf;kljasd;fljkas;lkdfja;lskjf;laksjdf;lkajsdf;laksjfl;kajsdfl;kjasdf;lkjasdf;kljasf;lkjas;dlfkjas;ldkfj test.', 'messageType': 'normal', 'postedTime': '2020-04-23T20:48:55.583Z', 'postedRoomId': 34, 'postedBy': {'id': 'eccac49d-cad2-4bf6-bd33-e9a232c407d1', 'displayName': 'Nick Hartung', 'url': 'http://hv-tfs:8080/tfs/Engineering Organization/_apis/Identities/eccac49d-cad2-4bf6-bd33-e9a232c407d1', 'imageUrl': 'http://hv-tfs:8080/tfs/Engineering Organization/_api/_common/identityImage?id=eccac49d-cad2-4bf6-bd33-e9a232c407d1'}}, {'id': 1108, 'content': 'This is another test.', 'messageType': 'normal', 'postedTime': '2020-04-23T21:14:31.48Z', 'postedRoomId': 34, 'postedBy': {'id': 'eccac49d-cad2-4bf6-bd33-e9a232c407d1', 'displayName': 'Nick Hartung', 'url': 'http://hv-tfs:8080/tfs/Engineering Organization/_apis/Identities/eccac49d-cad2-4bf6-bd33-e9a232c407d1', 'imageUrl': 'http://hv-tfs:8080/tfs/Engineering Organization/_api/_common/identityImage?id=eccac49d-cad2-4bf6-bd33-e9a232c407d1'}}, {'id': 1109, 'content': 'Hi team.', 'messageType': 'normal', 'postedTime': '2020-04-23T21:15:45.167Z', 'postedRoomId': 34, 'postedBy': {'id': 'eccac49d-cad2-4bf6-bd33-e9a232c407d1', 'displayName': 'Nick Hartung', 'url': 'http://hv-tfs:8080/tfs/Engineering Organization/_apis/Identities/eccac49d-cad2-4bf6-bd33-e9a232c407d1', 'imageUrl': 'http://hv-tfs:8080/tfs/Engineering Organization/_api/_common/identityImage?id=eccac49d-cad2-4bf6-bd33-e9a232c407d1'}}]
    return messages

def join_room(session, url, room_id, user_id):
    REST_PATH = f'/_apis/chat/rooms/{room_id}/users/{user_id}'
    _put_request(
        session, 
        url + REST_PATH, 
        data = {'UserId' : user_id}, 
        params = {'api-version' : '1.0'})

def leave_room(session, url, room_id, user_id):
    REST_PATH = f'/_apis/chat/rooms/{room_id}/users/{user_id}'
    _delete_request(
        session, 
        url + REST_PATH, 
        data = {'UserId' : user_id}, 
        params = {'api-version' : '1.0'})

def get_users(session, url, room_id):
    REST_PATH = f'/_apis/chat/rooms/{room_id}/users'
    messages = []
    data = _get_request(session, url + REST_PATH)
    if( data and data['count'] > 0 ):
        messages = data['value']
    return messages

def get_my_user_id(session, url):
    """
    This function uses an api that is undocumented in order to obtain the user 
    id. This api was discovered by monitoring the http calls made by the web 
    client.

    This undocumented api is being used in place of the documented /user/me api,
    which kept giving my errors. If the proper usage of /users/me is determined,
    it should be preferred in place of the unofficial api.
    """
    #  REST_PATH = f'/_apis/chat/rooms/{room_id}/users/me'
    REST_PATH = f'/_api/_Browse/GetCollectionProperties'
    data = _get_request(session, url + REST_PATH)
    return data['currentIdentity']['id']

def send_message(session, url, room_id, message):
    REST_PATH = f'/_apis/chat/rooms/{room_id}/messages'
    _post_request(
        session, 
        url + REST_PATH, 
        data = {'content' : message}, 
        params = {'api-version' : '1.0'})
