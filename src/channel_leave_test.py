from channel import channel_leave, channel_invite
from channels import channels_create
from auth import auth_register
from other import clear
import error
import pytest

# Setting up all the variables needed for test to run ############################################
clear()
Benjamin = auth_register("Benjamin@email.com", "password", "Benjamin", "Long")  # ID = 0
Ross = auth_register("Ross@email.com", "password", "Ross", "Short")             # ID = 1
Alex = auth_register("Alex@email.com", "password", "Alex", "Smith")             # ID = 2

channel_id0 = channels_create(Benjamin['token'], "Channel0", True)  # ID = 0
channel_id1 = channels_create(Ross['token'], "Channel1", True)     # ID = 1

# Everyone is in channel 0
channel_invite(Benjamin['token'], channel_id0, Ross['u_id'])
channel_invite(Benjamin['token'], channel_id0, Alex['u_id'])

# Ross and Alex are in channel 1 but not Benjamin
channel_invite(Ross['token'], channel_id1, Alex['u_id'])
##################################################################################################

def test_channel_leave_success():
    #Successful leave
    assert channel_leave(Benjamin['token'], channel_id0) == {}

def test_channel_leave_invalid_channel():
    #The channel doesn't exist
    #This should throw InputError
    with pytest.raises(error.InputError):
        assert channel_leave(Benjamin['token'], 2)

def test_channel_leave_not_a_member():
    #User is not part of this channel
    #This should throw AccessError
    with pytest.raises(error.AccessError):
        assert channel_leave(Benjamin['token'], channel_id1)

def test_invalid_token():
    #Token parsed in is invalid
    #This should throw AccessError
    with pytest.raises(error.AccessError):
        assert channel_leave("Booooop", channel_id1)