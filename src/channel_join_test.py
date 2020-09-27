from channel import channel_join, channel_invite
from channels import channels_create
from other import clear
import error
import pytest
from auth import auth_register

# Setting up all the variables needed for test to run ############################################
Benjamin = auth_register("Benjamin@email.com", "password", "Benjamin", "Long")  # ID = 0
Ross = auth_register("Ross@email.com", "password", "Ross", "Short")             # ID = 1
Alex = auth_register("Alex@email.com", "password", "Alex", "Smith")             # ID = 2

# Channel1 is a private channel
channels_create(Benjamin['token'], "Channel0", True)  # ID = 0
channels_create(Ross['token'], "Channel1", False)     # ID = 1

# Ross and Alex are in channel 1 but not Benjamin
channel_invite(Ross['token'], 1, 1)
channel_invite(Alex['token'], 1, 2)
##################################################################################################

def test_channel_join_success():
    clear()
    token = Benjamin['token']
    channel_id = 0
    assert channel_join(token, channel_id) == {}

def test_channel_join_invalid_channel():
    clear()
    #The channel doesn't exist
    #This should throw InputError
    token = Benjamin['token']
    channel_id = 2
    with pytest.raises(error.InputError):
        assert channel_join(token, channel_id)

def test_channel_join_not_a_member():
    clear()
    #Channel is private i.e. user is not admin
    #This should throw AccessError
    token = Benjamin['token']
    channel_id = 1
    with pytest.raises(error.AccessError):
        assert channel_join(token, channel_id)