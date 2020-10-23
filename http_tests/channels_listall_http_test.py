from url_fixture import url
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

# tests for listing one public channels
def test_channels_listall_public(url, initialisation):
    _, Ross, channel_id0, _ = initialisation
    r = requests.get(f'{url}/channels/listall', json={
        'token' : Ross['token']
    })
    assert payload['channels'] == {
        'channels' : [
            {
                "channel_id": 0,
                "name": "channel0",
            },
        ]
    }


# tests for listing one private channels
def test_channels_listall_private(url, initialisation):
    _, Ross, _, channel_id1 = initialisation
    r = requests.get(f'{url}/channels/listall', json={
        'token' : Ross['token']
    })
    assert payload['channels'] == {
        'channels' : [
            {
                "channel_id": 0,
                "name": "channe1",
            },
        ]
    }

# tests for listing one private channels
def test_channels_listsall_both(url, initialisation):
    _, Ross, channel_id0, channel_id1 = initialisation
    r = requests.get(f'{url}/channels/listall', json={
        'token' : Ross['token']
    })
    assert payload['channels'] == {
        'channels' : [
            {
                "channel_id": 0,
                "name": "channel0",
            },
            {
                "channel_id": 1,
                "name": "channel1",
            },
        ]
    }


# tests for listing many of each public and private channels
def test_channels_listsall_many():
    _, Ross, channel_id0, channel_id1 = initialisation
    channel2 = requests.post(f'{url}/channels/listall', json={
        'token' : Ross['token'],
        'name' : 'channel2',
        'is_public' : True,
    })
    channel3 = requests.post(f'{url}/channels/listall', json={
        'token' : Ross['token'],
        'name' : 'channel3',
        'is_public' : False,
    })
    assert payload['channels'] == {
        'channels' : [
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
    }