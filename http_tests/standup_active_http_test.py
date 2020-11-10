from url_fixture import url
import pytest
import requests
import urllib
import time

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

    # Alex to join public channel
    requests.post(f'{url}/channel/join', json={
        'token' : alex['token'],
        'channel_id' : channel0_id['channel_id'],
    })

    # Invites Alex to private channel
    requests.post(f'{url}/channel/invite', json={
        'token' : ross['token'],
        'channel_id' : channel1_id['channel_id'],
        'u_id' : alex['u_id'],
    })
    return benjamin, ross, alex, james, channel0_id, channel1_id

def test_standup_active_public(url, initialisation):
    Benjamin, _, Alex, _, channel_id0, _ = initialisation
    # Standup should last for 2 seconds
    r = requests.post(f'{url}/standup/start', json={
        'token' : Benjamin['token'],
        'channel_id' : channel_id0['channel_id'],
        'length' : 2,
    })
    end_time = r.json()
    time.sleep(1)
    ben_query_string = urllib.parse.urlencode({
        'token' : Benjamin['token'],
        'channel_id' : channel_id0['channel_id'],
    })
    alex_query_string = urllib.parse.urlencode({
        'token' : Alex['token'],
        'channel_id' : channel_id0['channel_id'],
    })
    r = requests.get(f'{url}/standup/active?{ben_query_string}')
    payload = r.json()
    assert payload == {'is_active': True, 'time_finish': end_time['time_finish']}
    r = requests.get(f'{url}/standup/active?{alex_query_string}')
    payload = r.json()
    assert payload == {'is_active': True, 'time_finish': end_time['time_finish']}
    time.sleep(1.5)
    r = requests.get(f'{url}/standup/active?{ben_query_string}')
    payload = r.json()
    assert payload == {'is_active': False, 'time_finish': None}
    r = requests.get(f'{url}/standup/active?{alex_query_string}')
    payload = r.json()
    assert payload == {'is_active': False, 'time_finish': None}

def test_standup_active_private(url, initialisation):
    _, Ross, Alex, _, _, channel_id1 = initialisation
    # Standup should last for 2 seconds
    r = requests.post(f'{url}/standup/start', json={
        'token' : Ross['token'],
        'channel_id' : channel_id1['channel_id'],
        'length' : 2,
    })
    end_time = r.json()
    time.sleep(1)
    ross_query_string = urllib.parse.urlencode({
        'token' : Ross['token'],
        'channel_id' : channel_id1['channel_id'],
    })
    alex_query_string = urllib.parse.urlencode({
        'token' : Alex['token'],
        'channel_id' : channel_id1['channel_id'],
    })
    r = requests.get(f'{url}/standup/active?{ross_query_string}')
    payload = r.json()
    assert payload == {'is_active': True, 'time_finish': end_time['time_finish']}
    r = requests.get(f'{url}/standup/active?{alex_query_string}')
    payload = r.json()
    assert payload == {'is_active': True, 'time_finish': end_time['time_finish']}
    time.sleep(1.5)
    r = requests.get(f'{url}/standup/active?{ross_query_string}')
    payload = r.json()
    assert payload == {'is_active': False, 'time_finish': None}
    r = requests.get(f'{url}/standup/active?{alex_query_string}')
    payload = r.json()
    assert payload == {'is_active': False, 'time_finish': None}

def test_standup_active_not_member(url, initialisation):
    Benjamin, _, _, James, channel_id0, _ = initialisation
    # Standup should last for 2 seconds
    requests.post(f'{url}/standup/start', json={
        'token' : Benjamin['token'],
        'channel_id' : channel_id0['channel_id'],
        'length' : 2,
    })
    time.sleep(1)
    query_string = urllib.parse.urlencode({
        'token' : James['token'],
        'channel_id' : channel_id0['channel_id'],
    })
    r = requests.get(f'{url}/standup/active?{query_string}')
    payload = r.json()
    assert payload['code'] == 400
    time.sleep(1.5)
    query_string = urllib.parse.urlencode({
        'token' : James['token'],
        'channel_id' : channel_id0['channel_id'],
    })
    r = requests.get(f'{url}/standup/active?{query_string}')
    payload = r.json()
    assert payload['code'] == 400

def test_standup_active_invalid_channel(url, initialisation):
    Benjamin, _, _, _, channel_id0, _ = initialisation
    requests.post(f'{url}/standup/start', json={
        'token' : Benjamin['token'],
        'channel_id' : channel_id0['channel_id'],
        'length' : 2,
    })
    time.sleep(1)
    query_string = urllib.parse.urlencode({
        'token' : Benjamin['token'],
        'channel_id' : 5,
    })
    r = requests.get(f'{url}/standup/active?{query_string}')
    payload = r.json()
    assert payload['code'] == 400

def test_standup_active_invalid_token(url, initialisation):
    Benjamin, _, _, _, channel_id0, _ = initialisation
    requests.post(f'{url}/standup/start', json={
        'token' : Benjamin['token'],
        'channel_id' : channel_id0['channel_id'],
        'length' : 2,
    })
    time.sleep(1)
    query_string = urllib.parse.urlencode({
        'token' : 'boop',
        'channel_id' : channel_id0['channel_id'],
    })
    r = requests.get(f'{url}/standup/active?{query_string}')
    payload = r.json()
    assert payload['code'] == 400
