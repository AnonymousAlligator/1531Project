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
        'is_public' : False,
    })
    channel1_id = channel1.json()

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
    return benjamin, ross, alex, channel0_id, channel1_id

def test_http_channel_details_public(url, initialisation):
    benjamin,_,_,channel0_id,_ = initialisation
    r = requests.get(f'{url}/channel/details', json={
        'token' : benjamin['token'],
        'channel_id' : channel0_id['channel_id'],
    })
    details = r.json()
    assert details['name'] == 'channel0'
    assert details['owner_members'] == [{'u_id': 0,
                                        'name_first':"Benjamin",
                                        'name_last': "Long",}]
    assert details['all_members'] == [{'u_id': 0,
                                        'name_first':"Benjamin",
                                        'name_last': "Long",},
                                    {'u_id': 1,
                                        'name_first':"Ross",
                                        'name_last': "Short",},
                                    {'u_id': 2,
                                        'name_first':"Alex",
                                        'name_last': "Smith",}]

def test_http_channel_details_private(url, initialisation):
    _,ross,_,_,channel1_id = initialisation
    r = requests.get(f'{url}/channel/details', json={
        'token' : ross['token'],
        'channel_id' : channel1_id['channel_id'],
    })
    details = r.json()
    assert details['name'] == 'channel1'
    assert details['owner_members'] == [{'u_id': 1,
                                        'name_first':"Ross",
                                        'name_last': "Short",},]
    assert details['all_members'] == [{'u_id': 1,
                                        'name_first':"Ross",
                                        'name_last': "Short",},
                                    {'u_id': 2,
                                        'name_first':"Alex",
                                        'name_last': "Smith",}]

def test_http_channel_details_invalid_channel(url, initialisation):
    #The channel doesn't exist
    #This should throw InputError
    benjamin,_,_,_,_ = initialisation
    r = requests.get(f'{url}/channel/details', json={
        'token' : benjamin['token'],
        'channel_id' : 2,
    })
    details = r.json()
    assert details['code'] == 400

def test_http_channel_details_not_a_member(url, initialisation):
    #User not a member of the channel
    #This should throw AccessError
    benjamin,_,_,_,channel1_id = initialisation
    r = requests.get(f'{url}/channel/details', json={
        'token' : benjamin['token'],
        'channel_id' : channel1_id['channel_id'],
    })
    details = r.json()
    assert details['code'] == 400

def test_http_invalid_token(url, initialisation):
    #Token parsed in is invalid
    #This should throw AccessError
    _,_,_,_,channel1_id = initialisation
    r = requests.get(f'{url}/channel/details', json={
        'token' : 'boooop',
        'channel_id' : channel1_id['channel_id'],
    })
    details = r.json()
    assert details['code'] == 400
