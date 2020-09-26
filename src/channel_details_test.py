from channel import channel_details, channel_invite, channel_addowner
from channels import channels_create
from auth import auth_register
import error
import pytest

# Setting up all the variables needed for test to run ############################################
Benjamin = auth_register("Benjamin@email.com", "password", "Benjamin", "Long")  # ID = 0
Ross = auth_register("Ross@email.com", "password", "Ross", "Short")             # ID = 1
Alex = auth_register("Alex@email.com", "password", "Alex", "Smith")             # ID = 2

channels_create(Benjamin['token'], "Channel0", True)  # ID = 0
channels_create(Ross['token'], "Channel1", False)     # ID = 1

# Everyone is in channel 0, Benjamin is owner
channel_invite(Benjamin['token'], 0, 0)
channel_invite(Ross['token'], 0, 1)
channel_invite(Alex['token'], 0, 2)
channel_addowner(Benjamin['token'], 0, 0)

# Ross and Alex are in channel 1, Ross is owner
channel_invite(Ross['token'], 1, 1)
channel_invite(Alex['token'], 1, 2)
channel_addowner(Ross['token'], 1, 1)
##################################################################################################

def test_channel_details_public():
    details = channel_details(Benjamin['token'], 0)
    assert details['name'] == 'Channel0'
    assert details['owner_members'] == 'Benjamin Long'
    assert details['all_members'] == ['Benjamin Long', 'Ross Short', 'Alex Smith']

def test_channel_details_private():
    details = channel_details(Ross['token'], 1)
    assert details['name'] == 'Channel1'
    assert details['owner_members'] == 'Ross Short'
    assert details['all_members'] == ['Ross Short', 'Alex Smith']

def test_channel_details_invalid_channel():
    #The channel doesn't exist
    #This should throw InputError
    token = Benjamin['token']
    channel_id = 2
    with pytest.raises(error.InputError):
        assert channel_details(token, channel_id)

def test_channel_details_not_a_member():
    #User not a member of the channel
    #This should throw AccessError
    token = Benjamin['token']
    channel_id = 1
    with pytest.raises(error.AccessError):
        assert channel_details(token, channel_id)