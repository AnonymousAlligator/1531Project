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
    benjamin = user0.json()
    user1 = requests.post(f'{url}/auth/register', json={
        'email' : 'Ross@email.com',
        'password' : 'password',
        'name_first' : 'Ross',
        'name_last' : 'Short',
    })
    ross = user1.json()

    # Create channels
    channel0 = requests.post(f'{url}/channels/create', json={
        'token' : benjamin['token'],
        'name' : 'channel0',
        'is_public' : True,
    })
    channel0_id = channel0.json()

    channel1 = requests.post(f'{url}/channels/create', json={
        'token' : ross['token'],
        'name' : 'channel0',
        'is_public' : True,
    })
    channel1_id = channel1.json()

    # Place users into relevant channels
    requests.post(f'{url}/channel/join', json={
        'token' : ross['token'],
        'channel_id' : channel0_id['channel_id'],
    })

    requests.post(f'{url}/channel/join', json={
        'token' : benjamin['token'],
        'channel_id' : channel1_id['channel_id'],
    })
    return benjamin, ross, channel0_id, channel1_id


# check that editing a message works
def test_message_edit(url, initialisation):

    benjamin, _, channel0_id, _ = initialisation
            
    message0 = "initial message"
    message_edited = "final message"

    r = requests.post(f'{url}/message/send', json={
        'token' : benjamin['token'],
        'channel_id' : channel0_id['channel_id'],
        'message' : message0,
    })

    message = r.json()

    r = requests.put(f'{url}/message/edit', json={
        'token' : benjamin['token'],
        'message_id' : message['message_id'],
        'message' : message_edited,
    })

    payload = r.json()

    assert payload == {}

# check that user1 cannot edit user0's message
def test_message_edit_notusermsg(url, initialisation):

    benjamin, ross, channel0_id, _ = initialisation
        
    message0 = "benjamin's message"
    message_edited = "final edited message"

    r = requests.post(f'{url}/message/send', json={
        'token' : benjamin['token'],
        'channel_id' : channel0_id['channel_id'],
        'message' : message0,
    })

    message = r.json()

    r = requests.put(f'{url}/message/edit', json={
        'token' : ross['token'],
        'message_id' : message['message_id'],
        'message' : message_edited,
    })

    payload = r.json()
    assert payload['code'] == 400

def test_message_edit_msgdoesnotexist(url, initialisation):

    benjamin, _, channel0_id, _ = initialisation

    message0 = "benjamin's message"
    message_edited = "final edited message"

    r = requests.post(f'{url}/message/send', json={
        'token' : benjamin['token'],
        'channel_id' : channel0_id['channel_id'],
        'message' : message0,
    })

    message = r.json()

    r = requests.put(f'{url}/message/edit', json={
        'token' : benjamin['token'],
        'message_id' : 2,
        'message' : message_edited,
    })

    payload = r.json()
    assert payload['code'] == 400

def test_message_edit_emptymsg(url, initialisation):

    benjamin, ross, channel0_id, _ = initialisation

    message0 = "initial message"
    message_edited = "    "

    r = requests.post(f'{url}/message/send', json={
        'token' : benjamin['token'],
        'channel_id' : channel0_id['channel_id'],
        'message' : message0,
    })

    message = r.json()

    r = requests.put(f'{url}/message/edit', json={
        'token' : benjamin['token'],
        'message_id' : message['message_id'],
        'message' : message_edited,
    })

    payload = r.json()

    assert payload == {}

def test_message_edit_channelowner(url, initialisation):

    benjamin, ross, channel0_id, _ = initialisation

    message0 = "initial message"
    message_edited = "final edited message"

    requests.post(f'{url}/channel/addowner', json={
        'token' : benjamin['token'],
        'channel_id' : channel0_id['channel_id'],
        'u_id' : ross['u_id'],
    })

    r = requests.post(f'{url}/message/send', json={
        'token' : benjamin['token'],
        'channel_id' : channel0_id['channel_id'],
        'message' : message0,
    })

    message = r.json()


    r = requests.put(f'{url}/message/edit', json={
        'token' : ross['token'],
        'message_id' : message['message_id'],
        'message' : message_edited,
    })

    payload = r.json()

    assert payload == {}

def test_message_edit_token(url, initialisation):

    benjamin, _, channel0_id, _ = initialisation
            
    message0 = "initial message"
    message_edited = "final message"

    r = requests.post(f'{url}/message/send', json={
        'token' : benjamin['token'],
        'channel_id' : channel0_id['channel_id'],
        'message' : message0,
    })

    message = r.json()

    r = requests.put(f'{url}/message/edit', json={
        'token' : 'hello',
        'message_id' : message['message_id'],
        'message' : message_edited,
    })

    payload = r.json()

    assert payload['code'] == 400
