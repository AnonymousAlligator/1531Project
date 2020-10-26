
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
    user3 = requests.post(f'{url}/auth/register', json={
        'email' : 'James@email.com',
        'password' : 'password',
        'name_first' : 'James',
        'name_last' : 'Smith',
    })
    james = user3.json()

    # Create channels
    channel0 = requests.post(f'{url}/channels/create', json={
        'token' : ross['token'],
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


    # Benjamin to join public channe
    requests.post(f'{url}/channel/join', json={
        'token' : benjamin['token'],
        'channel_id' : channel0_id['channel_id'],
    })

    # Invites Alex to private channel
    requests.post(f'{url}/channel/invite', json={
        'token' : ross['token'],
        'channel_id' : channel1_id['channel_id'],
        'u_id' : alex['u_id'],
    })
    return benjamin, ross, alex, james, channel0_id, channel1_id


# tests for listing one public channels
def test_channels_list_one_user_channel(url, initialisation):
    Benjamin, _, _, _, _, _ = initialisation

    query_string = urllib.parse.urlencode({
        'token' : Benjamin['token'],
    })
    r = requests.get(f'{url}/channels/list?{query_string}')

    payload = r.json()
    assert payload['channels'] == [
            {
                "channel_id": 0,
                "name": "channel0",
            },
        ]

# tests for listing 2 public channels
def test_channels_list(url, initialisation):
    _, Ross, _, _, _, _ = initialisation

    query_string = urllib.parse.urlencode({
        'token' : Ross['token'],
    })
    r = requests.get(f'{url}/channels/list?{query_string}')
    payload = r.json()
    assert payload['channels'] == [
            {
                "channel_id": 0,
                "name": "channel0",
            },
            {
                "channel_id": 1,
                "name": "channel1",
            },
        ]

# user0 creates 1 public, 1 private channel. user1 joins only 1 private channel.
# check that for user1, only return the private channel they are part of
def test_channels_list_authorised_priv_channel(url, initialisation):
    _, _, Alex, _, _, _ = initialisation

    query_string = urllib.parse.urlencode({
        'token' : Alex['token'],
    })
    r = requests.get(f'{url}/channels/list?{query_string}')
    payload = r.json()
    assert payload['channels'] == [
            {
                "channel_id": 1,
                "name": "channel1",
            },
        ]

# user0 and user1 both create one of each public and private channels. user1 joins all 4 channels.
# check that for user0, return only the 2 channels they created
def test_channels_list_joined_channels(url, initialisation):
    _, Ross, _, James, channel_id0, channel_id1 = initialisation

    requests.post(f'{url}/channels/create', json={
        'token' : James['token'],
        'name' : 'channel2',
        'is_public' : True,
    })

    requests.post(f'{url}/channels/create', json={
        'token' : James['token'],
        'name' : 'channel3',
        'is_public' : False,
    })

    requests.post(f'{url}/channel/invite', json={
        'token' : Ross['token'],
        'channel_id' : channel_id1['channel_id'],
        'u_id' : James['u_id'],
    })

    requests.post(f'{url}/channel/join', json={
        'token' : James['token'],
        'channel_id' : channel_id0['channel_id'],
    })


    query_string = urllib.parse.urlencode({
        'token' : James['token'],
    })
    r = requests.get(f'{url}/channels/list?{query_string}')
    payload = r.json()
    assert payload['channels'] ==[
            {
                "channel_id": 0,
                "name": "channel0",
            },
            {
                "channel_id": 1,
                "name": "channel1",
            },
            {
                "channel_id": 2,
                "name": "channel2",
            },            
            {
                "channel_id": 3,
                "name": "channel3",
            },
        ]

def test_channels_list_token_error(url, initialisation):
    _, _, _, _, _, _ = initialisation
    query_string = urllib.parse.urlencode({
        'token' : 'boop',
    })
    r = requests.get(f'{url}/channels/listall?{query_string}')
    payload = r.json()
    assert payload['code'] == 400
