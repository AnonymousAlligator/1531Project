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

    channel2 = requests.post(f'{url}/channels/create', json={
        'token' : ross['token'],
        'name' : 'channel2',
        'is_public' : True,
    })
    channel2_id = channel2.json()

    # Benjamin to join public channe
    requests.post(f'{url}/channel/join', json={
        'token' : benjamin['token'],
        'channel_id' : channel0_id['channel_id'],
    })
    # Alex to join public channe
    requests.post(f'{url}/channel/join', json={
        'token' : alex['token'],
        'channel_id' : channel0_id['channel_id'],
    })
    # James to join public channe
    requests.post(f'{url}/channel/join', json={
        'token' : james['token'],
        'channel_id' : channel0_id['channel_id'],
    })
    #alex to join public channel
    requests.post(f'{url}/channel/join', json={
        'token' : alex['token'],
        'channel_id' : channel2_id['channel_id'],
    })

    # Invites Alex to private channel
    requests.post(f'{url}/channel/invite', json={
        'token' : ross['token'],
        'channel_id' : channel1_id['channel_id'],
        'u_id' : alex['u_id'],
    })

    #Makes Alex an owner of private channel
    r = requests.post(f'{url}/channel/addowner', json={
        'token' : ross['token'],
        'channel_id' : channel1_id['channel_id'],
        'u_id' : alex['u_id'],
    })

    return benjamin, ross, alex, james, channel0_id, channel1_id, channel2_id

def test_channel_removeowner_success(url, initialisation):
    Benjamin, Ross, _, _, channel_id0, _, _ = initialisation
    r = requests.post(f'{url}/channel/removeowner', json={
        'token' : Ross['token'],
        'channel_id' : channel_id0['channel_id'],
        'u_id' : Benjamin['u_id'],
    })
    payload = r.json()
    assert payload == {}

#Successfully removed themselves as owner
def test_channel_removeowner_owner_success(url, initialisation):
    Benjamin, Ross, _, _, channel_id0, _, _ = initialisation
    r = requests.post(f'{url}/channel/removeowner', json={
        'token' : Benjamin['token'],
        'channel_id' : channel_id0['channel_id'],
        'u_id' : Benjamin['u_id'],
    })
    payload = r.json()
    assert payload == {}

#Successfully removing owner who is part of a private channel
def test_channel_removeowner_invited(url, initialisation):
    _, Ross, Alex, _, _, channel_id1, _ = initialisation
    r = requests.post(f'{url}/channel/removeowner', json={
        'token' : Ross['token'],
        'channel_id' : channel_id1['channel_id'],
        'u_id' : Alex['u_id'],
    })
    payload = r.json()
    assert payload == {}


#Channel does not exist
def test_channel_removeowner_invalid_channel(url, initialisation):
    Benjamin, Ross, _, _, channel_id0, _, _, = initialisation    
    r = requests.post(f'{url}/channel/removeowner', json={
        'token' : Ross['token'],
        'channel_id' : 4,
        'u_id' : Benjamin['u_id'],
    })
    payload = r.json()
    assert payload['code'] == 400

#Attempting to remove owner when the caller is not an owner.
def test_channel_removeowner_caller_not_owner(url, initialisation):
    Benjamin, _, Alex, _, channel_id0, _, _, = initialisation
    r = requests.post(f'{url}/channel/removeowner', json={
        'token' : Alex['token'],
        'channel_id' : channel_id0['channel_id'],
        'u_id' : Benjamin['u_id'],
    })
    payload = r.json()
    assert payload['code'] == 400


#Attempting to remove owner when the person called is not an owner.
def test_channel_removeowner_not_owner(url, initialisation):
    Benjamin, _, Alex, _, channel_id0, _, _, = initialisation
    r = requests.post(f'{url}/channel/removeowner', json={
        'token' : Benjamin['token'],
        'channel_id' : channel_id0['channel_id'],
        'u_id' : Alex['u_id'],
    })
    payload = r.json()
    assert payload['code'] == 400

#Attempting to remove owner when neither caller or person called is owner.
def test_channel_removeowner_neither_owner(url, initialisation):
    _, Ross, Alex, James, channel_id0, _, _, = initialisation
    r = requests.post(f'{url}/channel/removeowner', json={
        'token' : James['token'],
        'channel_id' : channel_id0['channel_id'],
        'u_id' : Alex['u_id'],
    })
    payload = r.json()
    assert payload['code'] == 400    

#Owner removing themselves as owner when there is only one owner but other members
def test_channel_removeowner_only_owner(url, initialisation):
    _, Ross, _, _, _, _, channel_id2,= initialisation
    r = requests.post(f'{url}/channel/removeowner', json={
        'token' : Ross['token'],
        'channel_id' : channel_id2['channel_id'],
        'u_id' : Ross['u_id'],
    })
    payload = r.json()
    print(payload)
    assert payload['code'] == 400

#Owner removing themselves as owner when there is no other member in the channel and they are the only owner.
def test_channel_removeowner_only_member(url, initialisation):
    Benjamin, Ross, _, _, _, _, channel_id2,= initialisation
    requests.post(f'{url}/channel/leave', json={
        'token' : 'Benjamin',
        'channel_id' : channel_id2['channel_id'],
    })

    r = requests.post(f'{url}/channel/removeowner', json={
        'token' : Ross['token'],
        'channel_id' : channel_id2['channel_id'],
        'u_id' : Ross['u_id'],
    })
    payload = r.json()
    assert payload['code'] == 400    
#Attempting to remove owner when the person called is NOT part of private channel
def test_channel_removeowner_not_invited(url, initialisation):
    Benjamin, Ross, Alex, _, _, channel_id1, _,= initialisation
    r = requests.post(f'{url}/channel/removeowner', json={
        'token' : Ross['token'],
        'channel_id' : channel_id1['channel_id'],
        'u_id' : Benjamin['u_id'],
    })
    payload = r.json()
    assert payload['code'] == 400   