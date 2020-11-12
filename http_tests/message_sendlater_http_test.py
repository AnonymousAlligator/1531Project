from url_fixture import url
import pytest
import requests
from datetime import datetime
from time import sleep
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
        'token' : benjamin['token'],
        'name' : 'channel1',
        'is_public' : True,
    })
    channel1_id = channel1.json()

    # Place users into relevant channels
    requests.post(f'{url}/channel/invite', json={
        'token' : benjamin['token'],
        'channel_id' : channel0_id['channel_id'],
        'u_id' : ross['u_id'],
    })
    return benjamin, ross, channel0_id, channel1_id

#Checking message ID's are sent in assigned in order
def test_message_sendlater_in_order(url, initialisation):
    test_user_0, test_user_1, channel_name1,_ = initialisation
    message = "hi"
    requests.post(f'{url}/message/sendlater', json={
        'token' : test_user_1['token'],
        'channel_id' : channel_name1['channel_id'],
        'message' : message,
        'time_sent': (datetime.now()).timestamp()+2,
    })
    requests.post(f'{url}/message/send', json={
        'token' : test_user_1['token'],
        'channel_id' : channel_name1['channel_id'],
        'message' : message,
    })
    requests.post(f'{url}/message/send', json={
        'token' : test_user_1['token'],
        'channel_id' : channel_name1['channel_id'],
        'message' : message,
    })
    requests.post(f'{url}/message/sendlater', json={
        'token' : test_user_0['token'],
        'channel_id' : channel_name1['channel_id'],
        'message' : message,
        'time_sent': (datetime.now()).timestamp()+4,
    })
    sleep(2.5)
    r = requests.post(f'{url}/message/send', json={
        'token' : test_user_1['token'],
        'channel_id' : channel_name1['channel_id'],
        'message' : message,
    })
    payload = r.json()
    assert payload == {'message_id': 3}
    sleep(2.5)
    r = requests.post(f'{url}/message/send', json={
        'token' : test_user_1['token'],
        'channel_id' : channel_name1['channel_id'],
        'message' : message,
    })
    payload = r.json()
    assert payload == {'message_id': 5}

#Successfully sending message exactly 1000 characters
def test_message_sendlater_exactly1000chars(url, initialisation):
    test_user_0, _, channel_name1,_ = initialisation
    message = "hi"*500
    requests.post(f'{url}/message/sendlater', json={
        'token' : test_user_0['token'],
        'channel_id' : channel_name1['channel_id'],
        'message' : message,
        'time_sent': (datetime.now()).timestamp()+1,
    })
    sleep(1.5)
    r = requests.post(f'{url}/message/send', json={
        'token' : test_user_0['token'],
        'channel_id' : channel_name1['channel_id'],
        'message' : message,
    })
    payload = r.json()
    assert payload == {'message_id': 1}

#Attempting to send an empty message
def test_message_sendlater_message_empty(url, initialisation):
    test_user_0, _, channel_name1,_ = initialisation
    message = ""
    r = requests.post(f'{url}/message/sendlater', json={
        'token' : test_user_0['token'],
        'channel_id' : channel_name1['channel_id'],
        'message' : message,
        'time_sent': (datetime.now()).timestamp()+1,
    })
    payload = r.json()
    assert payload['code'] == 400

#Attempting to send a message with only spaces
def test_message_sendlater_message_spaces(url, initialisation):
    test_user_0, _, channel_name1,_ = initialisation
    message = "   "
    r = requests.post(f'{url}/message/sendlater', json={
        'token' : test_user_0['token'],
        'channel_id' : channel_name1['channel_id'],
        'message' : message,
        'time_sent': (datetime.now()).timestamp()+1,
    })
    payload = r.json()
    assert payload['code'] == 400

#Attempting to send a message with over 1000 characters
def test_message_sendlater_morethan1000chars(url, initialisation):
    test_user_0, _, channel_name1,_ = initialisation
    message = "hi"*502
    r = requests.post(f'{url}/message/sendlater', json={
        'token' : test_user_0['token'],
        'channel_id' : channel_name1['channel_id'],
        'message' : message,
        'time_sent': (datetime.now()).timestamp()+1,
    })
    payload = r.json()
    assert payload['code'] == 400

#Attempting to send a message when the user is not in the channel
def test_message_sendlater_usernotinchannel(url, initialisation):
    _, test_user_1,_,channel_name2 = initialisation
    message = "hi"
    r = requests.post(f'{url}/message/sendlater', json={
        'token' : test_user_1['token'],
        'channel_id' : channel_name2['channel_id'],
        'message' : message,
        'time_sent': (datetime.now()).timestamp()+1,
    })
    payload = r.json()
    assert payload['code'] == 400

def test_message_sendlater_invalid_token(url, initialisation):
    _,_,_,channel_name2 = initialisation
    message = "hi"
    r = requests.post(f'{url}/message/sendlater', json={
        'token' : 'boop',
        'channel_id' : channel_name2['channel_id'],
        'message' : message,
        'time_sent': (datetime.now()).timestamp()+1,
    })
    payload = r.json()
    assert payload['code'] == 400

def test_message_sendlater_invalid_channel_id(url, initialisation):
    _,test_user_1,_,_ = initialisation
    message = "hi"
    r = requests.post(f'{url}/message/sendlater', json={
        'token' : test_user_1['token'],
        'channel_id' : 4,
        'message' : message,
        'time_sent': (datetime.now()).timestamp()+1,
    })
    payload = r.json()
    assert payload['code'] == 400
