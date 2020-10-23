from url_fixture import url
import pytest
import requests
import urllib

@pytest.fixture
def initialisation(url):
    # Clear data space
    requests.delete(f'{url}/clear')

    # Register users
    test_user0 = requests.post(f'{url}/auth/register', json={
        "email" : "testemail0@email.com",
        "password" : "valid_pw0",
        "name_first" : "Hayden",
        "name_last" : "Jacobs",
    })
    test_user0 = test_user0.json()       
    test_user1 = requests.post(f'{url}/auth/register', json={
        "email" : "testemail1@email.com",
        "password" : "valid_pw1",
        "name_first" : "Jayden",
        "name_last" : "Haycobs",
    })
    test_user1 = test_user1.json()

    # Create channels
    channel0 = requests.post(f'{url}/channels/create', json={
        'token' : test_user0['token'],
        'name' : 'channel0',
        'is_public' : True,
    })

    channel_id0 = channel0.json()
    
    channel1 = requests.post(f'{url}/channels/create', json={
        'token' : test_user0['token'],
        'name' : 'channel1',
        'is_public' : True,
    })

    channel_id1 = channel1.json()
    # Send messages
    requests.post(f'{url}/message/send', json={
            'token' : test_user0['token'],
            'channel_id' : channel_id0['channel_id'],
            'message' : "Let's geddit",
    })
    
    requests.post(f'{url}/message/send', json={
            'token' : test_user0['token'],
            'channel_id' : channel_id0['channel_id'],
            'message' : "Let's go",
    })

    requests.post(f'{url}/message/send', json={
            'token' : test_user0['token'],
            'channel_id' : channel_id1['channel_id'],
            'message' : "Hello",
    })

    requests.post(f'{url}/message/send', json={
        'token' : test_user0['token'],
        'channel_id' : channel_id1['channel_id'],
        'message' : "Hi",
    })

    requests.post(f'{url}/message/send', json={
            'token' : test_user0['token'],
            'channel_id' : channel_id1['channel_id'],
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

    return test_user0, test_user1, expectedmessages0, expectedmessages1, channel_id0, channel_id1

def test_search_single(url, initialisation):
    user0, _, _, _, _, _ = initialisation

    query_string = urllib.parse.urlencode({
        'token' : user0['token'],
        'query_str': "geddit",
    })

    r = requests.get(f'{url}/search?{query_string}')

    payload = r.json()
    messages = payload['messages']
    for msg in messages:
        assert msg['message_id'] == 0
        assert msg['channel_id'] == 0
        assert msg['u_id'] == 0
        assert msg['message'] == "Let's geddit"

def test_search_multiplecase(url, initialisation):
    user0, _, _, expectedmessages0, _, _ = initialisation

    query_string = urllib.parse.urlencode({
        'token' : user0['token'],
        'query_str': "let's",
    })
    r = requests.get(f'{url}/search?{query_string}')

    payload = r.json()
    messages = payload['messages']

    for i, msg in enumerate(messages):
        assert msg['message_id'] == expectedmessages0[i]['message_id']
        assert msg['u_id'] == expectedmessages0[i]['u_id']
        assert msg['message'] == expectedmessages0[i]['message']

def test_search_multiplediffchannel(url, initialisation):
    user0, _, _, expectedmessages1, _, _ = initialisation

    query_string = urllib.parse.urlencode({
        'token' : user0['token'],
        'query_str': "e",
    })
    r = requests.get(f'{url}/search?{query_string}')

    payload = r.json()
    messages = payload['messages']

    for i, msg in enumerate(messages):
        assert msg['message_id'] == expectedmessages1[i]['message_id']
        assert msg['channel_id'] == expectedmessages1[i]['channel_id']
        assert msg['u_id'] == expectedmessages1[i]['u_id']
        assert msg['message'] == expectedmessages1[i]['message']

def test_search_multiplestring(url, initialisation):
    user0, _, _, _, _, _ = initialisation

    query_string = urllib.parse.urlencode({
        'token' : user0['token'],
        'query_str': "ahahhaaha",
    })
    r = requests.get(f'{url}/search?{query_string}')

    payload = r.json()
    messages = payload['messages']

    assert messages == []

def test_search_notapartofchannel(url, initialisation):
    _, user1, _, _, _, _ = initialisation

    query_string = urllib.parse.urlencode({
        'token' : user1['token'],
        'query_str': "e",
    })
    r = requests.get(f'{url}/search?{query_string}')

    payload = r.json()
    messages = payload['messages']

    assert messages == []

def test_search_notapartofchannel(url, initialisation):
    _, _, _, _, _, _ = initialisation

    query_string = urllib.parse.urlencode({
        'token' : 'hello',
        'query_str': "hello",
    })
    r = requests.get(f'{url}/search?{query_string}')
    
    details = r.json()
    assert details['code'] == 400

