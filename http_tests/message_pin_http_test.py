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

    # Create channels
    channel0 = requests.post(f'{url}/channels/create', json={
        'token' : user0['token'],
        'name' : 'channel0',
        'is_public' : True,
    })
    channel0_id = channel0.json()

    message0 = "inital message"
    r = requests.post(f'{url}/message/send', json={
        'token' : user0['token'],
        'channel_id' : channel0_id['channel_id'],
        'message' : message0,
    })
    message0_id = r.json()

    channel1 = requests.post(f'{url}/channels/create', json={
        'token' : user1['token'],
        'name' : 'channel1',
        'is_public' : True,
    })
    channel1_id = channel1.json()

    r = requests.post(f'{url}/message/send', json={
        'token' : user1['token'],
        'channel_id' : channel1_id['channel_id'],
        'message' : message0,
    })
    message1_id = r.json()

    return user0, user1, message0_id, message1_id

def test_message_pin(url, initialisation):
    user0, _, message0_id, _ = initialisation
    r = requests.post(f'{url}/message/pin', json={
        'token' : user0['token'],
        'message_id' : message0_id['message_id'],
    })
    payload = r.json()
    assert payload == {}

def test_message_pin_notmember(url, initialisation):
    user0, _, _, message1_id = initialisation
    r = requests.post(f'{url}/message/pin', json={
        'token' : user0['token'],
        'message_id' : message1_id['message_id'],
    })
    payload = r.json()

    assert payload['code'] == 400

def test_message_pin_owner(url, initialisation):
    user0, user1, message0_id, _ = initialisation
    r = requests.post(f'{url}/channel/invite', json={
        'token' : user0['token'],
        'channel_id' : 0,
        'u_id' : user1['u_id'],
    })

    r = requests.post(f'{url}/message/pin', json ={
        'token' : user1['token'],
        'message_id' : message0_id['message_id']
    })
    payload = r.json()

    assert payload['code'] == 400

def test_message_pin_invalidmsgid(url, initialisation):
    user0, _, _, _ = initialisation
    r = requests.post(f'{url}/message/pin', json={
        'token' : user0['token'],
        'message_id' : 2,
    })
    payload = r.json()

    assert payload['code'] == 400

def test_message_pin_alreadypinned(url, initialisation):
    user0, _, message0_id, _ = initialisation
    r = requests.post(f'{url}/message/pin', json={
        'token' : user0['token'],
        'message_id' : message0_id['message_id'],
    })

    r = requests.post(f'{url}/message/pin', json={
        'token' : user0['token'],
        'message_id' : message0_id['message_id'],
    })

    payload = r.json()
    assert payload['code'] == 400

def test_message_pin_invalidtoken(url, initialisation):
    _, _, message0_id, _ = initialisation
    r = requests.post(f'{url}/message/pin', json={
        'token' : 'hello',
        'message_id' : message0_id['message_id'],
    })
    payload = r.json()

    assert payload['code'] == 400