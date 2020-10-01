from channel import channel_invite, channel_messages
from channels import channels_create
from auth import auth_register
from message import message_send
from other import clear, data
import error
import pytest

# Setting up all the variables needed for test to run ############################################
clear()
Benjamin = auth_register("Benjamin@email.com", "password", "Benjamin", "Long")  # ID = 0
Ross = auth_register("Ross@email.com", "password", "Ross", "Short")             # ID = 1
Alex = auth_register("Alex@email.com", "password", "Alex", "Smith")             # ID = 2

# Create and populate channel 0
channel_id0 = channels_create(Benjamin['token'], "Channel0", True)     # ID = 0
i = 0
expected_messages0 = []
while i < 50:
    data['channels'][0]['messages'].insert(0, {'message_id': i,'u_id': Benjamin['u_id'],'message': "hi",'time_created': i + 200})
    i += 1
while i < 100:
    message = {'message_id': i,'u_id': Benjamin['u_id'],'message': "bye",'time_created': i + 200}
    data['channels'][0]['messages'].insert(0, message)
    expected_messages0.insert(0, message)
    i += 1

# Create and populate channel 1
channel_id1 = channels_create(Benjamin['token'], "Channel1", True)     # ID = 1
i = 0
expected_messages1 = []
while i < 50:
    message = {'message_id': i,'u_id': 0,'message': "hello",'time_created': i + 200}
    data['channels'][1]['messages'].insert(0, message)
    expected_messages1.insert(0, message)
    i += 1

# Create and populate channel 2
channel_id2 = channels_create(Benjamin['token'], "Channel2", True)     # ID = 2
i = 0
expected_messages2 = []
while i < 10:
    message = {'message_id': i,'u_id': 0,'message': "why",'time_created': i + 200}
    data['channels'][2]['messages'].insert(0, message)
    expected_messages2.insert(0, message)
    i += 1
expected_messages3 = [expected_messages2[9]]

# Create and populate channel 3
channel_id3 = channels_create(Ross['token'], "Channel3", True)        # ID = 3
i = 0
while i < 50:
    message = {'message_id': i,'u_id': 1,'message': "why",'time_created': i + 200}
    data['channels'][3]['messages'].insert(0, message)
    i += 1

# Channel 0 will have 100 messages
channel_invite(Ross['token'], channel_id0, Ross['u_id'])
channel_invite(Alex['token'], channel_id0, Alex['u_id'])

# Channel 1 will have 50 messages
channel_invite(Ross['token'], channel_id1, Ross['u_id'])
channel_invite(Alex['token'], channel_id1, Alex['u_id'])

# Channel 2 will have 10 messages
channel_invite(Ross['token'], channel_id2, Ross['u_id'])
channel_invite(Alex['token'], channel_id2, Alex['u_id'])

# Channel 3 used to test AccessError
channel_invite(Alex['token'], channel_id3, Alex['u_id'])
##################################################################################################

def test_channel_messages_100():
    messages = channel_messages(Benjamin['token'], channel_id0, 0)
    assert messages['messages'] == expected_messages0
    assert messages['start'] == 0
    assert messages['end'] == 50

def test_channel_messages_50():
    messages = channel_messages(Benjamin['token'], channel_id1, 0)
    assert messages['messages'] == expected_messages1
    assert messages['start'] == 0
    assert messages['end'] == 50

def test_channel_messages_10():
    messages = channel_messages(Benjamin['token'], channel_id2, 0)
    assert messages['messages'] == expected_messages2
    assert messages['start'] == 0
    assert messages['end'] == 10

def test_channel_messages_no_more():
    messages = channel_messages(Benjamin['token'], channel_id2, 9)
    assert messages['messages'] == 'why'
    assert messages['start'] == 9
    assert messages['end'] == -1

def test_channel_messages_invalid_channel():
    #The channel doesn't exist
    #This should throw InputError
    with pytest.raises(error.InputError):
        assert channel_messages(Benjamin['token'], 4, 0)

def test_channel_messages_invalid_start():
    #Start is greater than total
    #This should throw InputError
    with pytest.raises(error.InputError):
        assert channel_messages(Benjamin['token'], channel_id2, 11)

def test_channel_messages_not_a_member():
    #User not a member of the channel
    #This should throw AccessError
    with pytest.raises(error.AccessError):
        assert channel_messages(Benjamin['token'], channel_id3, 3)

def test_invalid_token():
    #Token parsed in is invalid
    #This should throw AccessError
    with pytest.raises(error.AccessError):
        assert channel_messages("Booooop", channel_id1, 1)