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
        'is_public' : True,
    })
    channel1_id = channel1.json()
    channel2 = requests.post(f'{url}/channels/create', json={
        'token' : benjamin['token'],
        'name' : 'channel2',
        'is_public' : True,
    })
    channel2_id = channel2.json()
    channel3 = requests.post(f'{url}/channels/create', json={
        'token' : benjamin['token'],
        'name' : 'channel3',
        'is_public' : True,
    })
    channel3_id = channel3.json()

    # Place users into relevant channels
    requests.post(f'{url}/channel/invite', json={
        'token' : benjamin['token'],
        'channel_id' : channel0_id['channel_id'],
        'u_id' : ross['u_id'],
    })
    requests.post(f'{url}/channel/invite', json={
        'token' : benjamin['token'],
        'channel_id' : channel0_id['channel_id'],
        'u_id' : alex['u_id'],
    })
    requests.post(f'{url}/channel/invite', json={
        'token' : ross['token'],
        'channel_id' : channel1_id['channel_id'],
        'u_id' : alex['u_id'],
    })
    requests.post(f'{url}/channel/invite', json={
        'token' : benjamin['token'],
        'channel_id' : channel2_id['channel_id'],
        'u_id' : ross['u_id'],
    })
    requests.post(f'{url}/channel/invite', json={
        'token' : benjamin['token'],
        'channel_id' : channel2_id['channel_id'],
        'u_id' : alex['u_id'],
    })
    requests.post(f'{url}/channel/addowner', json={
        'token' : benjamin['token'],
        'channel_id' : channel2_id['channel_id'],
        'u_id' : ross['u_id'],
    })
    return benjamin, ross, alex, channel0_id, channel1_id, channel2_id, channel3_id

def test_multiple_owners(url, initialisation):
    benjamin, _, _, _, _, channel2_id, _ = initialisation
    # Person leaving is owner but there are other owners
    r = requests.post(f'{url}/channel/leave', json={
        'token' : benjamin['token'],
        'channel_id' : channel2_id['channel_id'],
    })
    payload = r.json()
    assert payload == {}
def test_only_owner_alone(url, initialisation):
    benjamin, _, _, _, _, _, channel3_id = initialisation
    # Person is owner but is only member so they can leave
    r = requests.post(f'{url}/channel/leave', json={
        'token' : benjamin['token'],
        'channel_id' : channel3_id['channel_id'],
    })
    payload = r.json()
    assert payload == {}

def test_is_member(url, initialisation):
    _, _, alex, channel0_id, _, _, _ = initialisation
    # Person leaving is just a member
    r = requests.post(f'{url}/channel/leave', json={
        'token' : alex['token'],
        'channel_id' : channel0_id['channel_id'],
    })
    payload = r.json()
    assert payload == {}

def test_channel_leave_invalid_channel(url, initialisation):
    benjamin, _, _, _, _, _, _ = initialisation
    #The channel doesn't exist
    #This should throw InputError
    r = requests.post(f'{url}/channel/leave', json={
        'token' : benjamin['token'],
        'channel_id' : 4,
    })
    payload = r.json()
    assert payload['code'] == 400

def test_channel_leave_not_a_member(url, initialisation):
    benjamin, _, _, _, channel1_id, _, _ = initialisation
    #User is not part of this channel
    #This should throw AccessError
    r = requests.post(f'{url}/channel/leave', json={
        'token' : benjamin['token'],
        'channel_id' : channel1_id['channel_id'],
    })
    payload = r.json()
    assert payload['code'] == 400

def test_invalid_token(url, initialisation):
    _, _, _, _, channel1_id, _, _ = initialisation
    #Token parsed in is invalid
    #This should throw AccessError
    r = requests.post(f'{url}/channel/leave', json={
        'token' : 'boop',
        'channel_id' : channel1_id['channel_id'],
    })
    payload = r.json()
    assert payload['code'] == 400

def test_only_owner(url, initialisation):
    # Person leaving is the only owner but there are other members
    # Should be input error
    benjamin, _, _, channel0_id, _, _, _ = initialisation
    r = requests.post(f'{url}/channel/leave', json={
        'token' : benjamin['token'],
        'channel_id' : channel0_id['channel_id'],
    })
    payload = r.json()
    assert payload['code'] == 400
