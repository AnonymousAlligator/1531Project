from url_fixture import url
import pytest
import requests

@pytest.fixture
def initialisation(url):
    # Clear data space
    requests.delete(f'{url}/clear')

    # Register users
    user0 = requests.post(f'{url}/auth/register', json={
        'email' : 'Benjamin@email.com',
        'password' : 'password',
        'name_first' : 'Benjamin',
        'name_last' : 'Long',
    })
    user0 = user0.json()       
    user1 = requests.post(f'{url}/auth/register', json={
        'email' : 'Ross@email.com',
        'password' : 'password',
        'name_first' : 'Ross',
        'name_last' : 'Short',
    })
    user1 = user1.json()

    # Create channels
    channel0 = requests.post(f'{url}/channels/create', json={
        'token' : benjamin['token'],
        'name' : 'channel0',
        'is_public' : True,
    })
    
    channel1 = requests.post(f'{url}/channels/create', json={
        'token' : benjamin['token'],
        'name' : 'channel1',
        'is_public' : True,
    })
    # Send messages
    requests.post(f'{url}/message/send', json={
            'token' : user0['token'],
            'channel_id' : channel_id0['channel_id'],
            'message' : "Let's geddit",
        })
    
    requests.post(f'{url}/message/send', json={
            'token' : user0['token'],
            'channel_id' : channel_id0['channel_id'],
            'message' : "Let's go",
        })

    requests.post(f'{url}/message/send', json={
            'token' : user0['token'],
            'channel_id' : channel_id0['channel_id'],
            'message' : "Hello",
        })

    requests.post(f'{url}/message/send', json={
        'token' : user0['token'],
        'channel_id' : channel_id0['channel_id'],
        'message' : "Hi",
    })

    requests.post(f'{url}/message/send', json={
            'token' : user0['token'],
            'channel_id' : channel_id0['channel_id'],
            'message' : "Hey",
        })
    # Set up lists of expected messages
    expectedmessages0 = [{'message_id': 1,
                    'channel_id': 0,
                    'u_id': 0,
                    'message': "Let's go"},
                    {'message_id': 0,
                    'channel_id': 0,
                    'u_id': 0,
                    'message': "Let's geddit"},]

    expectedmessages1 = [{'message_id': 4,
                    'channel_id': 1,
                    'u_id': 0,
                    'message': "Hey"},
                    {'message_id': 2,
                    'channel_id': 1,
                    'u_id': 0,
                    'message': "Hello"},
                    {'message_id': 1,
                    'channel_id': 0,
                    'u_id': 0,
                    'message': "Let's go"},
                    {'message_id': 0,
                    'channel_id': 0,
                    'u_id': 0,
                    'message': "Let's geddit"}]

    return user0, user1, expectedmessages0, expectedmessages1

def test_search_single(url, initialisation):
    user0, _, _, _ = initialisation()

    query_string = urllib.parse.urlencode({
        'token' : user0['token'],
        'query_str': "geddit"
    })
    r = requests.get(f'{url}/search?{query_str}')
    payload = r.json()
    for msg in payload['messages']:
        assert msg['message_id'] == 0
        assert msg['channel_id'] == 0
        assert msg['u_id'] == 0
        assert msg['message'] == "Let's geddit"