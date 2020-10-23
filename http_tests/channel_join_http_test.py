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
    user2 = requests.post(f'{url}/auth/register', json={
        'email' : 'Alex@email.com',
        'password' : 'password',
        'name_first' : 'Alex',
        'name_last' : 'Smith',
    })
    alex = user2.json()
    user3 = requests.post(f'{url}/auth/register', json={
        'email' : 'James@email.com',
        'password' : 'password',
        'name_first' : 'James',
        'name_last' : 'Smith',
    })
    james = user3.json()

    # Create channels
    channel0 = requests.post(f'{url}/channels/create', json={
        'token' : benjamin['token'],
        'name' : 'channel0',
        'is_public' : True,
    })
    channel0_id = channel0.json()
    channel1 = requests.post(f'{url}/channels/create', json={
        'token' : ross['token'],
        'name' : 'channel1',
        'is_public' : False,
    })
    channel1_id = channel1.json()

    # Place users into relevant channels
    requests.post(f'{url}/channel/invite', json={
        'token' : ross['token'],
        'channel_id' : channel1_id['channel_id'],
        'u_id' : alex['u_id'],
    })
    return benjamin, ross, alex, james, channel0_id, channel1_id

def test_channel_join_success(url, initialisation):
    _, Ross, _, _, channel_id0, _ = initialisation
    r = requests.post(f'{url}/channel/join', json={
        'token' : Ross['token'],
        'channel_id' : channel_id0['channel_id'],
    })
    payload = r.json()
    assert payload == {}

def test_channel_join_flockr_owner(url, initialisation):
    Benjamin, _, _, _, _, channel_id1 = initialisation
    #permission_id is 1 so person can join private channels and added as an owner
    r = requests.post(f'{url}/channel/join', json={
        'token' : Benjamin['token'],
        'channel_id' : channel_id1['channel_id'],
    })
    payload = r.json()
    assert payload == {}

def test_channel_join_invalid_channel(url, initialisation):
    Benjamin, _, _, _, _, _ = initialisation
    #The channel doesn't exist
    #This should throw InputError
    r = requests.post(f'{url}/channel/join', json={
        'token' : Benjamin['token'],
        'channel_id' : 2,
    })
    payload = r.json()
    assert payload['code'] == 400

def test_channel_join_not_a_member(url, initialisation):
    _, _, _, James, _, channel_id1 = initialisation
    #Channel is private i.e. user is not admin
    #This should throw AccessError
    r = requests.post(f'{url}/channel/join', json={
        'token' : James['token'],
        'channel_id' : channel_id1['channel_id'],
    })
    payload = r.json()
    assert payload['code'] == 400

def test_invalid_token(url, initialisation):
    _, _, _, _, _, channel_id1 = initialisation
    #Token parsed in is invalid
    #This should throw AccessError
    r = requests.post(f'{url}/channel/join', json={
        'token' : 'boop',
        'channel_id' : channel_id1['channel_id'],
    })
    payload = r.json()
    assert payload['code'] == 400
