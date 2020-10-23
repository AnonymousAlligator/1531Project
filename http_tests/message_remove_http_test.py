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
    public_channel_id = channel0.json()
    channel1 = requests.post(f'{url}/channels/create', json={
        'token' : ross['token'],
        'name' : 'channel1',
        'is_public' : False,
    })
    private_channel_id = channel1.json()
    channel2 = requests.post(f'{url}/channels/create', json={
        'token' : ross['token'],
        'name' : 'channel2',
        'is_public' : True,
    })
    public_channel_id2 = channel2.json()
    # Place users into relevant channels
    requests.post(f'{url}/channel/invite', json={
        'token' : benjamin['token'],
        'channel_id' : public_channel_id['channel_id'],
        'u_id' : ross['u_id'],
    })
    requests.post(f'{url}/channel/invite', json={
        'token' : benjamin['token'],
        'channel_id' : public_channel_id['channel_id'],
        'u_id' : alex['u_id'],
    })
    requests.post(f'{url}/channel/invite', json={
        'token' : ross['token'],
        'channel_id' : private_channel_id['channel_id'],
        'u_id' : alex['u_id'],
    })
    requests.post(f'{url}/channel/invite', json={
        'token' : ross['token'],
        'channel_id' : public_channel_id2['channel_id'],
        'u_id' : alex['u_id'],
    })
    return benjamin, ross, alex, public_channel_id, private_channel_id, public_channel_id2

# check func works when 1 user (owner) in public channel, sends 1 message and removes it
def test_message_remove_works_public(url, initialisation):
    test_user0, _, _, public_channel_id, _, _ = initialisation
    # test_user0 sends 1 message to public channel
    message0 = "Let's geddit"
    r = requests.post(f'{url}/message/send', json={
        'token' : test_user0['token'],
        'channel_id' : public_channel_id['channel_id'],
        'message' : message0,
    })
    message0_id = r.json()
    # assert func works for public channel
    r = requests.delete(f'{url}/message/remove', json={
        'token' : test_user0['token'],
        'message_id' : message0_id['message_id'],
    })
    payload = r.json()
    assert payload == {}

# check func works when 1 user (owner) in private channel, sends 1 message and removes it
def test_message_remove_works_private(url, initialisation):
    _, test_user1, _, _, private_channel_id, _ = initialisation
    # test_user0 sends 1 message to public channel
    message0 = "Let's geddit"
    r = requests.post(f'{url}/message/send', json={
        'token' : test_user1['token'],
        'channel_id' : private_channel_id['channel_id'],
        'message' : message0,
    })
    message0_id = r.json()
    # assert func works for public channel
    r = requests.delete(f'{url}/message/remove', json={
        'token' : test_user1['token'],
        'message_id' : message0_id['message_id'],
    })
    payload = r.json()
    assert payload == {}

# check func works when 2 users in channel, user1 (not owner) sends message and removes it
def test_message_remove_works_more_people_channel(url, initialisation):
    _, test_user1, _, public_channel_id, _, _ = initialisation
    # test_user1 sends 1 message to public channel
    message0 = "Let's geddit"
    r = requests.post(f'{url}/message/send', json={
        'token' : test_user1['token'],
        'channel_id' : public_channel_id['channel_id'],
        'message' : message0,
    })
    message0_id = r.json()
    # assert func works for public channel
    r = requests.delete(f'{url}/message/remove', json={
        'token' : test_user1['token'],
        'message_id' : message0_id['message_id'],
    })
    payload = r.json()
    assert payload == {}

# check channel owner can remove messages
def test_message_remove_channel_owner(url, initialisation):
    test_user0, test_user1, _, public_channel_id, _, _ = initialisation
    # test_user1 sends 1 message to public channel
    message0 = "Let's geddit"
    r = requests.post(f'{url}/message/send', json={
        'token' : test_user1['token'],
        'channel_id' : public_channel_id['channel_id'],
        'message' : message0,
    })
    message0_id = r.json()
    # assert func works for public channel
    r = requests.delete(f'{url}/message/remove', json={
        'token' : test_user0['token'],
        'message_id' : message0_id['message_id'],
    })
    payload = r.json()
    assert payload == {}

# check flockr owner can remove messages
def test_message_remove_flockr_owner(url, initialisation):
    test_user0, test_user1, _, _, _, public_channel_id2 = initialisation
    # test_user1 sends 1 message to public channel
    message0 = "Let's geddit"
    r = requests.post(f'{url}/message/send', json={
        'token' : test_user1['token'],
        'channel_id' : public_channel_id2['channel_id'],
        'message' : message0,
    })
    message0_id = r.json()
    # assert func works for public channel
    r = requests.delete(f'{url}/message/remove', json={
        'token' : test_user0['token'],
        'message_id' : message0_id['message_id'],
    })
    payload = r.json()
    assert payload == {}

# check user can't remove an already deleted message
def test_message_remove_already_deleted_msg(url, initialisation):
    test_user0, _, _, public_channel_id, _, _ = initialisation
    # test_user1 sends 1 message to public channel
    message0 = "Let's geddit"
    r = requests.post(f'{url}/message/send', json={
        'token' : test_user0['token'],
        'channel_id' : public_channel_id['channel_id'],
        'message' : message0,
    })
    message0_id = r.json()
    # assert func works for public channel
    r = requests.delete(f'{url}/message/remove', json={
        'token' : test_user0['token'],
        'message_id' : message0_id['message_id'],
    })
    r = requests.delete(f'{url}/message/remove', json={
        'token' : test_user0['token'],
        'message_id' : message0_id['message_id'],
    })
    payload = r.json()
    assert payload['code'] == 400

# check user0 can't remove user1's message
def test_message_remove_no_permission(url, initialisation):
    test_user0, test_user1, _, public_channel_id, _, _ = initialisation
    # test_user1 sends 1 message to public channel
    message0 = "Let's geddit"
    r = requests.post(f'{url}/message/send', json={
        'token' : test_user0['token'],
        'channel_id' : public_channel_id['channel_id'],
        'message' : message0,
    })
    message0_id = r.json()
    # assert func works for public channel
    r = requests.delete(f'{url}/message/remove', json={
        'token' : test_user1['token'],
        'message_id' : message0_id['message_id'],
    })
    payload = r.json()
    assert payload['code'] == 400

def test_message_remove_invalid_token(url, initialisation):
    test_user0, _, _, public_channel_id, _, _ = initialisation
    message0 = "Let's geddit"
    r = requests.post(f'{url}/message/send', json={
        'token' : test_user0['token'],
        'channel_id' : public_channel_id['channel_id'],
        'message' : message0,
    })
    message0_id = r.json()
    r = requests.delete(f'{url}/message/remove', json={
        'token' : 'boop',
        'message_id' : message0_id['message_id'],
    })
    payload = r.json()
    assert payload['code'] == 400
