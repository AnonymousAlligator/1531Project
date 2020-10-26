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

    # Create channels
    channel0 = requests.post(f'{url}/channels/create', json={
        'token' : ross['token'],
        'name' : 'channel0',
        'is_public' : True,
    })
    channel0_id = channel0.json()

    channel1 = requests.post(f'{url}/channels/create', json={
        'token' : benjamin['token'],
        'name' : 'channel1',
        'is_public' : False,
    })
    channel1_id = channel1.json()
    return benjamin, ross, channel0_id, channel1_id

# tests for listing all channels
def test_channels_listall_public(url, initialisation):
    _, Ross, _, _ = initialisation
    query_string = urllib.parse.urlencode({
        'token' : Ross['token'],
    })
    r = requests.get(f'{url}/channels/listall?{query_string}')
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
# token error
def test_channels_listall_token_error(url, initialisation):
    _, _, _, _ = initialisation
    query_string = urllib.parse.urlencode({
        'token' : 'boop',
    })
    r = requests.get(f'{url}/channels/listall?{query_string}')
    payload = r.json()
    assert payload['code'] == 400
