from channel import channel_invite, channel_messages
from channels import channels_create
from auth import auth_register
from message import message_send
from other import clear, data
import error
import pytest

# Setting up all the variables needed for test to run ############################################
def initialisation():
    clear()
    Benjamin = auth_register("Benjamin@email.com", "password", "Benjamin", "Long")  # ID = 0
    Ross = auth_register("Ross@email.com", "password", "Ross", "Short")             # ID = 1
    Alex = auth_register("Alex@email.com", "password", "Alex", "Smith")             # ID = 2

    # Create and populate channel 0
    channel_id0 = channels_create(Benjamin['token'], "Channel0", True)     # ID = 0
    i = 0
    expected_messages0 = []
    while i < 50:
        message = {'message_id': i,'u_id': Benjamin['u_id'],'message': "hi",'time_created': i + 200}
        data['channels'][channel_id0['channel_id']]['messages'].insert(0, message)
        i += 1
    while i < 100:
        message = {'message_id': i,'u_id': Benjamin['u_id'],'message': "bye",'time_created': i + 200}
        data['channels'][channel_id0['channel_id']]['messages'].insert(0, message)
        expected_messages0.insert(0, message)
        i += 1

    # Create and populate channel 1
    channel_id1 = channels_create(Benjamin['token'], "Channel1", True)     # ID = 1
    i = 0
    expected_messages1 = []
    while i < 50:
        message = {'message_id': i,'u_id': 0,'message': "hello",'time_created': i + 200}
        data['channels'][channel_id1['channel_id']]['messages'].insert(0, message)
        expected_messages1.insert(0, message)
        i += 1

    # Create and populate channel 2
    channel_id2 = channels_create(Benjamin['token'], "Channel2", True)     # ID = 2
    i = 0
    expected_messages2 = []
    while i < 10:
        message = {'message_id': i,'u_id': 0,'message': "why",'time_created': i + 200}
        data['channels'][channel_id2['channel_id']]['messages'].insert(0, message)
        expected_messages2.insert(0, message)
        i += 1
    expected_messages3 = [expected_messages2[9]]

    # Create and populate channel 3
    channel_id3 = channels_create(Ross['token'], "Channel3", True)        # ID = 3
    i = 0
    while i < 50:
        message = {'message_id': i,'u_id': 1,'message': "why",'time_created': i + 200}
        data['channels'][channel_id3['channel_id']]['messages'].insert(0, message)
        i += 1

    # Channel 0 will have 100 messages
    channel_invite(Benjamin['token'], channel_id0['channel_id'], Ross['u_id'])
    channel_invite(Benjamin['token'], channel_id0['channel_id'], Alex['u_id'])

    # Channel 1 will have 50 messages
    channel_invite(Benjamin['token'], channel_id1['channel_id'], Ross['u_id'])
    channel_invite(Benjamin['token'], channel_id1['channel_id'], Alex['u_id'])

    # Channel 2 will have 10 messages
    channel_invite(Benjamin['token'], channel_id2['channel_id'], Ross['u_id'])
    channel_invite(Benjamin['token'], channel_id2['channel_id'], Alex['u_id'])

    # Channel 3 used to test AccessError
    channel_invite(Ross['token'], channel_id3['channel_id'], Alex['u_id'])

    return Benjamin, Ross, Alex, channel_id0, channel_id1, channel_id2, channel_id3, expected_messages0, expected_messages1, expected_messages2, expected_messages3
##################################################################################################

def test_channel_messages_100():
    Benjamin, _, _, channel_id0, _, _, _, expected_messages0, _, _, _ = initialisation()
    messages = channel_messages(Benjamin['token'], channel_id0['channel_id'], 0)
    assert messages['messages'] == expected_messages0
    assert messages['start'] == 0
    assert messages['end'] == 50

def test_channel_messages_50():
    Benjamin, _, _, _, channel_id1, _, _, _, expected_messages1, _, _ = initialisation()
    messages = channel_messages(Benjamin['token'], channel_id1['channel_id'], 0)
    assert messages['messages'] == expected_messages1
    assert messages['start'] == 0
    assert messages['end'] == 50

def test_channel_messages_10():
    Benjamin, _, _, _, _, channel_id2, _, _, _, expected_messages2, _ = initialisation()
    messages = channel_messages(Benjamin['token'], channel_id2['channel_id'], 0)
    assert messages['messages'] == expected_messages2
    assert messages['start'] == 0
    assert messages['end'] == 10

def test_channel_messages_no_more():
    Benjamin, _, _, _, _, channel_id2, _, _, _, _, expected_messages3 = initialisation()
    messages = channel_messages(Benjamin['token'], channel_id2['channel_id'], 9)
    assert messages['messages'] == expected_messages3
    assert messages['start'] == 9
    assert messages['end'] == -1

def test_channel_messages_invalid_channel():
    Benjamin, _, _, _, _, _, _, _, _, _, _ = initialisation()
    #The channel doesn't exist
    #This should throw InputError
    with pytest.raises(error.InputError):
        assert channel_messages(Benjamin['token'], 4, 0)

def test_channel_messages_invalid_start():
    Benjamin, _, _, _, _, channel_id2, _, _, _, _, _ = initialisation()
    #Start is greater than total
    #This should throw InputError
    with pytest.raises(error.InputError):
        assert channel_messages(Benjamin['token'], channel_id2['channel_id'], 11)

def test_channel_messages_not_a_member():
    Benjamin, _, _, _, _, _, channel_id3, _, _, _, _ = initialisation()
    #User not a member of the channel
    #This should throw AccessError
    with pytest.raises(error.AccessError):
        assert channel_messages(Benjamin['token'], channel_id3['channel_id'], 3)

def test_invalid_token():
    _, _, _, _, channel_id1, _, _, _, _, _, _ = initialisation()
    #Token parsed in is invalid
    #This should throw AccessError
    with pytest.raises(error.AccessError):
        assert channel_messages("Booooop", channel_id1['channel_id'], 1)