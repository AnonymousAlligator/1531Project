from channel import channel_invite, channel_messages
from channels import channels_create
from auth import auth_register
from message import message_send
import error
import pytest

# Setting up all the variables needed for test to run ############################################
Benjamin = auth_register("Benjamin@email.com", "password", "Benjamin", "Long")  # ID = 0
Ross = auth_register("Ross@email.com", "password", "Ross", "Short")             # ID = 1
Alex = auth_register("Alex@email.com", "password", "Alex", "Smith")             # ID = 2

# Create and populate channel 0
channels_create(Benjamin['token'], "Channel0", True)     # ID = 0
i = 0
expected_messages0 = []
while i < 50:
    message_send(Benjamin['token'], 0, "hi")
    i += 1
while i < 100:
    message_send(Benjamin['token'], 0, "bye")
    expected_messages0.append('bye')
    i += 1

# Create and populate channel 1
channels_create(Benjamin['token'], "Channel1", True)     # ID = 1
i = 0
expected_messages1 = []
while i < 50:
    message_send(Benjamin['token'], 0, "hello")
    expected_messages1.append('hello')
    i += 1

# Create and populate channel 2
channels_create(Benjamin['token'], "Channel2", True)     # ID = 2
i = 0
expected_messages2 = []
while i < 10:
    message_send(Benjamin['token'], 0, "why")
    expected_messages2.append('why')
    i += 1

# Create and populate channel 3
channels_create(Ross['token'], "Channel3", True)        # ID = 3
i = 0
while i < 50:
    message_send(Benjamin['token'], 0, "me")
    i += 1

# Channel 0 will have 100 messages
channel_invite(Benjamin['token'], 0, 0)
channel_invite(Ross['token'], 0, 1)
channel_invite(Alex['token'], 0, 2)

# Channel 1 will have 50 messages
channel_invite(Benjamin['token'], 1, 0)
channel_invite(Ross['token'], 1, 1)
channel_invite(Alex['token'], 1, 2)

# Channel 2 will have 10 messages
channel_invite(Benjamin['token'], 2, 0)
channel_invite(Ross['token'], 2, 1)
channel_invite(Alex['token'], 2, 2)

# Channel 3 used to test AccessError
channel_invite(Ross['token'], 6, 1)
channel_invite(Alex['token'], 6, 2)
##################################################################################################

def test_channel_messages_100():
    messages = channel_messages(Benjamin['token'], 0, 0)
    assert messages['messages'] == expected_messages0
    assert messages['start'] == 0
    assert messages['end'] == 50

def test_channel_messages_50():
    messages = channel_messages(Benjamin['token'], 1, 0)
    assert messages['messages'] == expected_messages1
    assert messages['start'] == 0
    assert messages['end'] == 50

def test_channel_messages_10():
    messages = channel_messages(Benjamin['token'], 2, 0)
    assert messages['messages'] == expected_messages2
    assert messages['start'] == 0
    assert messages['end'] == 10

def test_channel_messages_no_more():
    messages = channel_messages(Benjamin['token'], 2, 10)
    assert messages['messages'] == 'why'
    assert messages['start'] == 10
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
        assert channel_messages(Benjamin['token'], 2, 11)

def test_channel_messages_not_a_member():
    #User not a member of the channel
    #This should throw AccessError
    with pytest.raises(error.AccessError):
        assert channel_messages(Benjamin['token'], 2, 3)