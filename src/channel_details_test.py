from channel import channel_details, channel_invite
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
channel_id1 = channels_create(Ross['token'], "Channel1", False)     # ID = 1

# Everyone is in channel 0, Benjamin is owner
channel_invite(Ross['token'], channel_id0, Ross['u_id'])
channel_invite(Alex['token'], channel_id0, Alex['u_id'])

# Ross and Alex are in channel 1, Ross is owner
channel_invite(Alex['token'], channel_id1, Alex['u_id'])
##################################################################################################

def test_channel_details_public():
    details = channel_details(Benjamin['token'], channel_id0)
    assert details['name'] == 'Channel0'
    assert details['owner_members'] == 'Benjamin Long'
    assert details['all_members'] == ['Benjamin Long', 'Ross Short', 'Alex Smith']

def test_channel_details_private():
    details = channel_details(Ross['token'], channel_id1)
    assert details['name'] == 'Channel1'
    assert details['owner_members'] == 'Ross Short'
    assert details['all_members'] == ['Ross Short', 'Alex Smith']

def test_channel_details_invalid_channel():
    clear()
    #The channel doesn't exist
    #This should throw InputError
    with pytest.raises(error.InputError):
        assert channel_details(Benjamin['token'], 2)

def test_channel_details_not_a_member():
    clear()
    #User not a member of the channel
    #This should throw AccessError
    with pytest.raises(error.AccessError):
        assert channel_details(Benjamin['token'], channel_id1)