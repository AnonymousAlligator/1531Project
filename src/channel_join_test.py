from channel import channel_join, channel_invite
from channels import channels_create
from auth import auth_register
from other import clear
import error
import pytest

# Setting up all the variables needed for test to run ############################################
def initialisation():
    clear()
    Benjamin = auth_register("Benjamin@email.com", "password", "Benjamin", "Long")  # ID = 0
    Ross = auth_register("Ross@email.com", "password", "Ross", "Short")             # ID = 1
    Alex = auth_register("Alex@email.com", "password", "Alex", "Smith")             # ID = 2
    James = auth_register("James@email.com", "password", "James", "Smith")          # ID = 3

    # Channel1 is a private channel
    channel_id0 = channels_create(Benjamin['token'], "Channel0", True)  # ID = 0
    channel_id1 = channels_create(Ross['token'], "Channel1", False)     # ID = 1

    # Ross and Alex are in channel 1 but not Benjamin
    channel_invite(Ross['token'], channel_id1, Alex['u_id'])
    return Benjamin, Ross, Alex, James, channel_id0, channel_id1
##################################################################################################

def test_channel_join_success():
    _, Ross, _, _, channel_id0, _ = initialisation()
    assert channel_join(Ross['token'], channel_id0) == {}

def test_channel_join_invalid_channel():
    Benjamin, _, _, _, _, _ = initialisation()
    #The channel doesn't exist
    #This should throw InputError
    with pytest.raises(error.InputError):
        assert channel_join(Benjamin['token'], 2)

def test_channel_join_not_a_member():
    _, _, _, James, _, channel_id1 = initialisation()
    #Channel is private i.e. user is not admin
    #This should throw AccessError
    with pytest.raises(error.AccessError):
        assert channel_join(James['token'], channel_id1)

def test_channel_join_flockr_owner():
    Benjamin, _, _, _, _, channel_id1 = initialisation()
    #U_id is 0 so person can join private channels and added as an owner
    assert channel_join(Benjamin['token'], channel_id1) == {}

def test_invalid_token():
    _, _, _, _, _, _ = initialisation()
    #Token parsed in is invalid
    #This should throw AccessError
    with pytest.raises(error.AccessError):
        assert channel_join("Booooop", 1)