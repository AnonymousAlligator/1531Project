from url_fixture import url
import pytest
import requests
import urllib

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
    benjamin = user0.json()
    user1 = requests.post(f'{url}/auth/register', json={
        'email' : 'Ross@email.com',
        'password' : 'password',
        'name_first' : 'Ross',
        'name_last' : 'Short',
    })
    ross = user1.json()
    user2 = requests.post(f'{url}/auth/register', json={
        'email' : 'Alex@email.com',
        'password' : 'password',
        'name_first' : 'Alex',
        'name_last' : 'Smith',
    })
    alex = user2.json()

    # Create channels
    channel0 = requests.post(f'{url}/channels/create', json={
        'token' : benjamin['token'],
        'name' : 'channel0',
        'is_public' : True,
    })
    channel0_id = channel0.json()
    channel1 = requests.post(f'{url}/channels/create', json={
        'token' : benjamin['token'],
        'name' : 'channel1',
        'is_public' : True,
    })
    channel1_id = channel1.json()
    channel2 = requests.post(f'{url}/channels/create', json={
        'token' : benjamin['token'],
        'name' : 'channel2',
        'is_public' : True,
    })
    channel2_id = channel2.json()
    channel3 = requests.post(f'{url}/channels/create', json={
        'token' : ross['token'],
        'name' : 'channel3',
        'is_public' : True,
    })
    channel3_id = channel3.json()

    # Place users into relevant channels
    requests.post(f'{url}/channel/invite', json={
        'token' : benjamin['token'],
        'channel_id' : channel0_id['channel_id'],
        'u_id' : ross['u_id'],
    })
    requests.post(f'{url}/channel/invite', json={
        'token' : benjamin['token'],
        'channel_id' : channel0_id['channel_id'],
        'u_id' : alex['u_id'],
    })
    requests.post(f'{url}/channel/invite', json={
        'token' : benjamin['token'],
        'channel_id' : channel1_id['channel_id'],
        'u_id' : ross['u_id'],
    })
    requests.post(f'{url}/channel/invite', json={
        'token' : benjamin['token'],
        'channel_id' : channel1_id['channel_id'],
        'u_id' : alex['u_id'],
    })
    requests.post(f'{url}/channel/invite', json={
        'token' : benjamin['token'],
        'channel_id' : channel2_id['channel_id'],
        'u_id' : ross['u_id'],
    })
    requests.post(f'{url}/channel/invite', json={
        'token' : benjamin['token'],
        'channel_id' : channel2_id['channel_id'],
        'u_id' : alex['u_id'],
    })
    requests.post(f'{url}/channel/addowner', json={
        'token' : ross['token'],
        'channel_id' : channel2_id['channel_id'],
        'u_id' : alex['u_id'],
    })
    return benjamin, ross, alex, channel0_id, channel1_id, channel2_id, channel3_id

def test_channel_messages_100(url, initialisation):
    benjamin, _, _, channel_id0, _, _, _= initialisation
    i = 0
    expected_messages = []
    message = "hi"
    while i < 50:
        requests.post(f'{url}/message/send', json={
            'token' : benjamin['token'],
            'channel_id' : channel_id0['channel_id'],
            'message' : message,
        })
        i += 1
    message = "bye"
    while i < 100:
        r = requests.post(f'{url}/message/send', json={
            'token' : benjamin['token'],
            'channel_id' : channel_id0['channel_id'],
            'message' : message,
        })
        message_id = r.json()
        message_data = {'message_id': message_id['message_id'],
                        'u_id': benjamin['u_id'],
                        'message': "bye"}
        expected_messages.insert(0, message_data)
        i += 1
    query_string = urllib.parse.urlencode({
        'token' : benjamin['token'],
        'channel_id' : channel_id0['channel_id'],
        'start' : 0,
    })
    r = requests.get(f'{url}/channel/messages?{query_string}')
    payload = r.json()
    messages = payload['messages']
    for i, message_data in enumerate(messages):
        assert message_data['message_id'] == expected_messages[i]['message_id']
        assert message_data['u_id'] == expected_messages[i]['u_id']
        assert message_data['message'] == expected_messages[i]['message']
    assert payload['start'] == 0
    assert payload['end'] == 50

def test_channel_messages_50(url, initialisation):
    benjamin, _, _, _, channel_id1, _, _, = initialisation
    i = 0
    expected_messages = []
    message = "hello"
    while i < 50:
        r = requests.post(f'{url}/message/send', json={
            'token' : benjamin['token'],
            'channel_id' : channel_id1['channel_id'],
            'message' : message,
        })
        message_id = r.json()
        message_data = {'message_id': message_id['message_id'],
                        'u_id': benjamin['u_id'],
                        'message': "hello"}
        expected_messages.insert(0, message_data)
        i += 1
    query_string = urllib.parse.urlencode({
        'token' : benjamin['token'],
        'channel_id' : channel_id1['channel_id'],
        'start' : 0,
    })
    r = requests.get(f'{url}/channel/messages?{query_string}')
    payload = r.json()
    messages = payload['messages']
    for i, message_data in enumerate(messages):
        assert message_data['message_id'] == expected_messages[i]['message_id']
        assert message_data['u_id'] == expected_messages[i]['u_id']
        assert message_data['message'] == expected_messages[i]['message']
    assert payload['start'] == 0
    assert payload['end'] == 50

def test_channel_messages_10(url, initialisation):
    benjamin, _, _, _, _, channel_id2, _ = initialisation
    i = 0
    expected_messages = []
    message = "why"
    while i < 10:
        r = requests.post(f'{url}/message/send', json={
            'token' : benjamin['token'],
            'channel_id' : channel_id2['channel_id'],
            'message' : message,
        })
        message_id = r.json()
        message_data = {'message_id': message_id['message_id'],
                        'u_id': benjamin['u_id'],
                        'message': "why"}
        expected_messages.insert(0, message_data)
        i += 1
    query_string = urllib.parse.urlencode({
        'token' : benjamin['token'],
        'channel_id' : channel_id2['channel_id'],
        'start' : 0,
    })
    r = requests.get(f'{url}/channel/messages?{query_string}')
    payload = r.json()
    messages = payload['messages']
    for i, message_data in enumerate(messages):
        assert message_data['message_id'] == expected_messages[i]['message_id']
        assert message_data['u_id'] == expected_messages[i]['u_id']
        assert message_data['message'] == expected_messages[i]['message']
    assert payload['start'] == 0
    assert payload['end'] == 10

def test_channel_messages_no_more(url, initialisation):
    benjamin, _, _, _, _, channel_id2, _ = initialisation
    i = 0
    expected_messages = []
    message = "why"
    while i < 10:
        r = requests.post(f'{url}/message/send', json={
            'token' : benjamin['token'],
            'channel_id' : channel_id2['channel_id'],
            'message' : message,
        })
        if i == 0:
            message_id = r.json()
            message_data = {'message_id': message_id['message_id'],
                            'u_id': benjamin['u_id'],
                            'message': "why"}
            expected_messages.insert(0, message_data)
        i += 1
    query_string = urllib.parse.urlencode({
        'token' : benjamin['token'],
        'channel_id' : channel_id2['channel_id'],
        'start' : 9,
    })
    r = requests.get(f'{url}/channel/messages?{query_string}')
    payload = r.json()
    messages = payload['messages']
    for i, message_data in enumerate(messages):
        assert message_data['message_id'] == expected_messages[i]['message_id']
        assert message_data['u_id'] == expected_messages[i]['u_id']
        assert message_data['message'] == expected_messages[i]['message']
    assert payload['start'] == 9
    assert payload['end'] == -1

def test_channel_messages_invalid_channel(url, initialisation):
    benjamin, _, _, _, _, _, _ = initialisation
    #The channel doesn't exist
    #This should throw InputError
    query_string = urllib.parse.urlencode({
        'token' : benjamin['token'],
        'channel_id' : 4,
        'start' : 0,
    })
    r = requests.get(f'{url}/channel/messages?{query_string}')
    payload = r.json()
    assert payload['code'] == 400

def test_channel_messages_invalid_start(url, initialisation):
    benjamin, _, _, _, _, channel_id2, _ = initialisation
    #Start is greater than total
    #This should throw InputError
    i = 0
    message = "why"
    while i < 10:
        requests.post(f'{url}/message/send', json={
            'token' : benjamin['token'],
            'channel_id' : channel_id2['channel_id'],
            'message' : message,
        })
        i += 1
    query_string = urllib.parse.urlencode({
        'token' : benjamin['token'],
        'channel_id' : channel_id2['channel_id'],
        'start' : 11,
    })
    r = requests.get(f'{url}/channel/messages?{query_string}')
    payload = r.json()
    assert payload['code'] == 400

def test_channel_messages_not_a_member(url, initialisation):
    benjamin, _, _, _, _, _, channel_id3 = initialisation
    #User not a member of the channel
    #This should throw AccessError
    i = 0
    message = "jellooo"
    while i < 10:
        requests.post(f'{url}/message/send', json={
            'token' : benjamin['token'],
            'channel_id' : channel_id3['channel_id'],
            'message' : message,
        })
        i += 1
    query_string = urllib.parse.urlencode({
        'token' : benjamin['token'],
        'channel_id' : channel_id3['channel_id'],
        'start' : 0,
    })
    r = requests.get(f'{url}/channel/messages?{query_string}')
    payload = r.json()
    assert payload['code'] == 400

def test_invalid_token(url, initialisation):
    benjamin, _, _, _, channel_id1, _, _ = initialisation
    #Token parsed in is invalid
    #This should throw AccessError
    i = 0
    message = "jellooo"
    while i < 10:
        requests.post(f'{url}/message/send', json={
            'token' : benjamin['token'],
            'channel_id' : channel_id1['channel_id'],
            'message' : message,
        })
        i += 1
    query_string = urllib.parse.urlencode({
        'token' : 'boop',
        'channel_id' : channel_id1['channel_id'],
        'start' : 0,
    })
    r = requests.get(f'{url}/channel/messages?{query_string}')
    payload = r.json()
    assert payload['code'] == 400
    