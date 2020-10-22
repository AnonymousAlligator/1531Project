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

    user2 = requests.post(f'{url}/auth/register', json={
        "email" : "testemail2@email.com",
        "password" : "valid_pw1",
        "name_first" : "Nick",
        "name_last" : "Smith",
    })
    user2 = user2.json()

    # Create channels
    channel0 = requests.post(f'{url}/channels/create', json={
        'token' : user0['token'],
        'name' : 'channel0',
        'is_public' : True,
    })
    channel0_id = channel0.json()

    channel1 = requests.post(f'{url}/channels/create', json={
        'token' : user0['token'],
        'name' : 'channel1',
        'is_public' : False,
    })
    channel1_id = channel1.json()

    return user0, user1, user2, channel0_id, channel1_id

def test_channel_invite_owner_pass(url, initialisation):
    user0, user1, _, channel0_id, _ = initialisation
    r = requests.post(f'{url}/channel/invite', json={
        'token' : user0['token'],
        'channel_id' : channel0_id['channel_id'],
        'u_id' : user1['u_id']
    })
    payload = r.json()
    
    assert payload == {}

def test_channel_invite_member_pass(url, initialisation):
    user0, user1, user2, channel0_id, _ = initialisation
    r = requests.post(f'{url}/channel/invite', json={
        'token' : user0['token'],
        'channel_id' : channel0_id['channel_id'],
        'u_id' : user1['u_id']
    })
    r = requests.post(f'{url}/channel/invite', json={
        'token' : user1['token'],
        'channel_id' : channel0_id['channel_id'],
        'u_id' : user2['u_id']
    })
    payload = r.json()
    
    assert payload == {}