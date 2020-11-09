from url_fixture import url
import pytest
import requests

@pytest.fixture
def initialisation(url):
    #clear data
    requests.delete(f'{url}/clear')

    #register test users
    user0 = requests.post(f'{url}/auth/register', json={
        "email" : "testemail0@email.com",
        "password" : "valid_pw0",
        "name_first" : "Hayden",
        "name_last" : "Jacobs",
    })
    user0 = user0.json()

    user1 = requests.post(f'{url}/auth/register', json={
        "email" : "testemail1@email.com",
        "password" : "valid_pw1",
        "name_first" : "Jayden",
        "name_last" : "Haycobs",
    })
    user1 = user1.json()

    # user0 Create channels
    channel0 = requests.post(f'{url}/channels/create', json={
        'token' : user0['token'],
        'name' : 'channel0',
        'is_public' : True,
    })
    channel0_id = channel0.json()

    channel1 = requests.post(f'{url}/channels/create', json={
        'token' : user0['token'],
        'name' : 'channel1',
        'is_public' : True,
    })
    channel1_id = channel1.json()

    # user1 joins channel1 with user0
    requests.post(f'{url}/channel/join', json={
        'token' : user1['token'],
        'channel_id' : channel1_id,
    })
    
    # user1 creates channel
    channel2 = requests.post(f'{url}/channels/create', json={
        'token' : user1['token'],
        'name' : 'channel1',
        'is_public' : True,
    })
    channel2_id = channel2.json()
    
    return user0, user1, channel0_id, channel1_id, channel2_id
    
# check react works for one user, one message   
def test_message_react_one(url, initialisation):
    
    user0, _, channel0_id, _, _ = initialisation

    # user0 sends 1 message
    message = requests.post(f'{url}/message/send', json={
        'token' : user0['token'],
        'channel_id' : channel0_id['channel_id'],
        'message' : 'hi',
    })
    message_id = message.json()
    
    r = requests.post(f'{url}/message/react', json={
        'token' : user0['token'],
        'message_id' : message_id['message_id'],
        'react_id' : 1,
    })

    payload = r.json()
    assert payload == {}

# check react works for one user, two messages same channel
def test_message_react_two(url, initialisation):
    
    user0, _, channel0_id, _, _ = initialisation

    # user0 sends 2 messages
    message0 = requests.post(f'{url}/message/send', json={
        'token' : user0['token'],
        'channel_id' : channel0_id['channel_id'],
        'message' : 'hi',
    })
    message0_id = message0.json()

    message1 = requests.post(f'{url}/message/send', json={
        'token' : user0['token'],
        'channel_id' : channel0_id['channel_id'],
        'message' : 'hi',
    })
    message1_id = message1.json()
    
    # user0 reacts to 2 different messages
    requests.post(f'{url}/message/react', json={
        'token' : user0['token'],
        'message_id' : message0_id['message_id'],
        'react_id' : 1,
    })

    r = requests.post(f'{url}/message/react', json={
        'token' : user0['token'],
        'message_id' : message1_id['message_id'],
        'react_id' : 1,
    })

    payload = r.json()
    assert payload == {}

# check react works for one user, two messages diff channel
def test_message_react_two_diff(url, initialisation):
    
    user0, _, channel0_id, channel1_id, _ = initialisation

    # user0 sends 2 messages
    message0 = requests.post(f'{url}/message/send', json={
        'token' : user0['token'],
        'channel_id' : channel0_id['channel_id'],
        'message' : 'hi',
    })
    message0_id = message0.json()

    message1 = requests.post(f'{url}/message/send', json={
        'token' : user0['token'],
        'channel_id' : channel1_id['channel_id'],
        'message' : 'hi',
    })
    message1_id = message1.json()
    
    # user0 reacts to 2 different messages
    requests.post(f'{url}/message/react', json={
        'token' : user0['token'],
        'message_id' : message0_id['message_id'],
        'react_id' : 1,
    })

    r = requests.post(f'{url}/message/react', json={
        'token' : user0['token'],
        'message_id' : message1_id['message_id'],
        'react_id' : 1,
    })

    payload = r.json()
    assert payload == {}

# check react works for two users, one message   
def test_message_react_same(url, initialisation):
    
    user0, user1, _, channel1_id, _ = initialisation
    
    # user0 sends 1 messages into channel1
    message0 = requests.post(f'{url}/message/send', json={
        'token' : user0['token'],
        'channel_id' : channel1_id['channel_id'],
        'message' : 'hi',
    })
    message0_id = message0.json()

    # user0 reacts to message0
    requests.post(f'{url}/message/react', json={
        'token' : user0['token'],
        'message_id' : message0_id['message_id'],
        'react_id' : 1,
    })

    # user1 reacts to message0
    r = requests.post(f'{url}/message/react', json={
        'token' : user1['token'],
        'message_id' : message0_id['message_id'],
        'react_id' : 1,
    })

    payload = r.json()
    assert payload == {}

# check for error when invalid message_id
def test_message_react_invalid_message(url, initialisation):
    
    user0, _, _, _, _,  = initialisation
    
    # user1 reacts to invalid message_id
    r = requests.post(f'{url}/message/react', json={
        'token' : user0['token'],
        'message_id' : 123123,
        'react_id' : 1,
    })

    payload = r.json()
    assert payload['code'] == 400

# check for error when reacting to message in channel user is not in
def test_message_react_invalid_channel_member(url, initialisation):
    
    user0, user1, channel0_id, _, _ = initialisation
    
     # user0 sends 1 messages into channel0
    message0 = requests.post(f'{url}/message/send', json={
        'token' : user0['token'],
        'channel_id' : channel0_id['channel_id'],
        'message' : 'hi',
    })   

    message0_id = message0.json()

    # user1 reacts to message in channel0 which they are not part of
    r = requests.post(f'{url}/message/react', json={
        'token' : user1['token'],
        'message_id' : message0_id['message_id'],
        'react_id' : 1,
    })

    payload = r.json()
    assert payload['code'] == 400
