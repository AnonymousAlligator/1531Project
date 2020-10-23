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

    # Ross to join public channe
    requests.post(f'{url}/channel/join', json={
        'token' : ross['token'],
        'channel_id' : channel0_id['channel_id'],
    })
    # Alex to join public channe
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


def test_channel_addowner_success(url, initialisation):
    Benjamin, Ross, _, _, channel_id0, _ = initialisation
    r = requests.post(f'{url}/channel/addowner', json={
        'token' : Benjamin['token'],
        'channel_id' : channel_id0['channel_id'],
        'u_id' : Ross['u_id'],
    })
    payload = r.json()
    assert payload == {}

#Channel is private, user is part of private channel 
def test_channel_addowner_invited(url, initialisation):
    _, Ross, Alex, _, _, channel_id1 = initialisation
    r = requests.post(f'{url}/channel/addowner', json={
        'token' : Ross['token'],
        'channel_id' : channel_id1['channel_id'],
        'u_id' : Alex['u_id'],
    })
    payload = r.json()
    assert payload == {}

#Channel exists, token is NOT an owner, u_id is a member
def test_channel_addowner_not_owner(url, initialisation):
    Benjamin, _, Alex, _, channel_id0, _, = initialisation
    r = requests.post(f'{url}/channel/addowner', json={
        'token' : Benjamin,
        'channel_id' : channel_id0['channel_id'],
        'u_id' : Alex['u_id'],
    })
    payload = r.json()
    assert payload['code'] == 400

#Channel exists, token is NOT a member, u_id is a member
def test_adder_not_member(url, initialisation):
    Benjamin, _, _, James, channel_id0, _, = initialisation
    r = requests.post(f'{url}/channel/addowner', json={
        'token' : James,
        'channel_id' : channel_id0['channel_id'],
        'u_id' : Benjamin['u_id'],
    })
    payload = r.json()
    assert payload['code'] == 400   

#Channel exists, token is owner adding someone who is already a owner
def test_channel_addowner_already_owner(url, initialisation):
    Benjamin, Ross, _, _, channel_id0, _, = initialisation
    requests.post(f'{url}/channel/addowner', json={
        'token' : Ross,
        'channel_id' : channel_id0['channel_id'],
        'u_id' : Benjamin['u_id'],
    })

    r = requests.post(f'{url}/channel/addowner', json={
        'token' : Ross,
        'channel_id' : channel_id0['channel_id'],
        'u_id' : Benjamin['u_id'],
    })
    payload = r.json()
    assert payload['code'] == 400   

#Channel exists, token is adding themselves.
def test_channel_addowner_self(url, initialisation):
    _, Ross, _, _, channel_id0, _, = initialisation
    r = requests.post(f'{url}/channel/addowner', json={
        'token' : Ross,
        'channel_id' : channel_id0['channel_id'],
        'u_id' : Ross['u_id'],
    })
    payload = r.json()
    assert payload['code'] == 400   

#Channel does NOT exist, throw input error
def test_channel_addowner_invalid_channel(url, initialisation): 
    Benjamin, Ross, _, _, _, _, = initialisation
    r = requests.post(f'{url}/channel/addowner', json={
        'token' : Ross,
        'channel_id' : 4,
        'u_id' : Benjamin['u_id'],
    })
    payload = r.json()
    assert payload['code'] == 400   

#Channel is private, user is not part of private channel
def test_channel_addowner_not_invited(url, initialisation):
    _, Ross, _, James, _, channel_id1, = initialisation
    r = requests.post(f'{url}/channel/addowner', json={
        'token' : Ross,
        'channel_id' : channel_id1['channel_id'],
        'u_id' : James['u_id'],
    })
    payload = r.json()
    assert payload['code'] == 400   
