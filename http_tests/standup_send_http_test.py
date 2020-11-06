from url_fixture import url
from time import sleep
import pytest
import requests

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

# check standup_send with 1 active standup request works
def test_standup_send_one(url, initialisation):
        
    test_user_0, test_user_1, channel0_id,_ = initialisation    

    # user0 start 1 active standup
    requests.post(f'{url}/standup/start', json={
        'token' : test_user_0['token'],
        'channel_id' : channel0_id,
        'length': 3,
    })

    # user1 sends one message into standup
    r = requests.post(f'{url}/standup/send', json={
        'token' : test_user_1['token'],
        'channel_id' : channel0_id,
        'message' : 'hi',
    })

    payload = r.json()
    assert payload == {}


# check standup_send with multiple active standups(2) work
def test_standup_send_many(url, initialisation):

    test_user_0, test_user_1, channel0_id, channel1_id = initialisation    

    # start 2 active standups  
    # user1 start 1 active standup in channel0
    requests.post(f'{url}/standup/start', json={
        'token' : test_user_1['token'],
        'channel_id' : channel0_id,
        'length': 3,
    })

    # user0 start 1 active standup in channel1
    requests.post(f'{url}/standup/start', json={
        'token' : test_user_0['token'],
        'channel_id' : channel1_id,
        'length': 3,
    })

    # user0 sends one message into both standups
    requests.post(f'{url}/standup/send', json={
        'token' : test_user_0['token'],
        'channel_id' : channel0_id,
        'message' : 'hi channel0',
    })
    
    r = requests.post(f'{url}/standup/send', json={
        'token' : test_user_0['token'],
        'channel_id' : channel1_id,
        'message' : 'hi channel1',
    })

    payload = r.json()
    assert payload == {}

# check standup_send outside of active standup is invalid
def test_invalid_standup_send(url, initialisation):
    
    test_user_0, test_user_1, channel0_id,_ = initialisation    

    # user0 start 1 active standup
    requests.post(f'{url}/standup/start', json={
        'token' : test_user_0['token'],
        'channel_id' : channel0_id,
        'length': 1,
    })

    # ensure standup is over
    sleep(1)

    # user1 sends one message into standup
    r = requests.post(f'{url}/standup/send', json={
        'token' : test_user_1['token'],
        'channel_id' : channel0_id,
        'message' : 'hi',
    })

    payload = r.json()
    assert payload['code'] == 400