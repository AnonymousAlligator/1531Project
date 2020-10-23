from channel import channel_leave, channel_invite, channel_addowner
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

    channel_id0 = channels_create(Benjamin['token'], "Channel0", True)  # ID = 0
    channel_id1 = channels_create(Ross['token'], "Channel1", True)     # ID = 1
    channel_id2 = channels_create(Benjamin['token'], "Channel2", True)  # ID = 2
    channel_id3 = channels_create(Benjamin['token'], "Channel3", True)  # ID = 3

    # Everyone is in channel 0
    channel_invite(Benjamin['token'], channel_id0['channel_id'], Ross['u_id'])
    channel_invite(Benjamin['token'], channel_id0['channel_id'], Alex['u_id'])

    # Ross and Alex are in channel 1 but not Benjamin
    channel_invite(Ross['token'], channel_id1['channel_id'], Alex['u_id'])

    # Ben + Ross == Owner
    channel_invite(Benjamin['token'], channel_id2['channel_id'], Ross['u_id'])
    channel_invite(Benjamin['token'], channel_id2['channel_id'], Alex['u_id'])
    channel_addowner(Benjamin['token'],channel_id2['channel_id'], Ross['u_id'])

    # Ben is only member and owner of channel 3

    return Benjamin, Ross, Alex, channel_id0, channel_id1, channel_id2, channel_id3
##################################################################################################

def test_multiple_owners():
    Benjamin, _, _, _, _, channel_id2, _ = initialisation()
    # Person leaving is owner but there are other owners
    assert channel_leave(Benjamin['token'], channel_id2['channel_id']) == {}
def test_only_owner_alone():
    Benjamin, _, _, _, _, _, channel_id3 = initialisation()
    # Person is owner but is only member so they can leave
    assert channel_leave(Benjamin['token'], channel_id3['channel_id']) == {}

def test_is_member():
    _, _, Alex, channel_id0, _, _, _ = initialisation()
    # Person leaving is just a member
    assert channel_leave(Alex['token'], channel_id0['channel_id']) == {}

def test_channel_leave_invalid_channel():
    Benjamin, _, _, _, _, _, _ = initialisation()
    #The channel doesn't exist
    #This should throw InputError
    with pytest.raises(error.InputError):
        assert channel_leave(Benjamin['token'], 4)

def test_channel_leave_not_a_member():
    Benjamin, _, _, _, channel_id1, _, _ = initialisation()
    #User is not part of this channel
    #This should throw AccessError
    with pytest.raises(error.AccessError):
        assert channel_leave(Benjamin['token'], channel_id1['channel_id'])

def test_invalid_token():
    _, _, _, _, channel_id1, _, _ = initialisation()
    #Token parsed in is invalid
    #This should throw AccessError
    with pytest.raises(error.AccessError):
        assert channel_leave("Booooop", channel_id1['channel_id'])

def test_only_owner():
    # Person leaving is the only owner but there are other members
    # Should be input error
    Benjamin, _, _, channel_id0, _, _, _ = initialisation()
    with pytest.raises(error.InputError):
        assert channel_leave(Benjamin['token'], channel_id0['channel_id'])

