from channel import channel_details, channel_invite
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
    channel_id1 = channels_create(Ross['token'], "Channel1", False)     # ID = 1

    # Everyone is in channel 0, Benjamin is owner
    channel_invite(Benjamin['token'], channel_id0['channel_id'], Ross['u_id'])
    channel_invite(Benjamin['token'], channel_id0['channel_id'], Alex['u_id'])

    # Ross and Alex are in channel 1, Ross is owner
    channel_invite(Ross['token'], channel_id1['channel_id'], Alex['u_id'])
    return Benjamin, Ross, Alex, channel_id0, channel_id1
##################################################################################################

def test_channel_details_public():
    Benjamin, _, _, channel_id0, _ = initialisation()
    details = channel_details(Benjamin['token'], channel_id0['channel_id'])
    assert details['name'] == 'Channel0'
    assert details['owner_members'] == [{'u_id': 0,  
                                        'name_first':"Benjamin", 
                                        'name_last': "Long",}]
    assert details['all_members'] == [{'u_id': 0, 
                                        'name_first':"Benjamin", 
                                        'name_last': "Long",},
                                    {'u_id': 1,  
                                        'name_first':"Ross", 
                                        'name_last': "Short", },
                                    {'u_id': 2, 
                                        'name_first':"Alex", 
                                        'name_last': "Smith",}]

def test_channel_details_private():
    _, Ross, _, _, channel_id1 = initialisation()
    details = channel_details(Ross['token'], channel_id1['channel_id'])
    assert details['name'] == 'Channel1'
    assert details['owner_members'] == [{'u_id': 1,  
                                        'name_first':"Ross", 
                                        'name_last': "Short", },]
    assert details['all_members'] == [{'u_id': 1,  
                                        'name_first':"Ross", 
                                        'name_last': "Short", },
                                    {'u_id': 2, 
                                        'name_first':"Alex", 
                                        'name_last': "Smith",}]

def test_channel_details_invalid_channel():
    Benjamin, _, _, _, _ = initialisation()
    #The channel doesn't exist
    #This should throw InputError
    with pytest.raises(error.InputError):
        assert channel_details(Benjamin['token'], 2)

def test_channel_details_not_a_member():
    Benjamin, _, _, _, channel_id1 = initialisation()
    #User not a member of the channel
    #This should throw AccessError
    with pytest.raises(error.AccessError):
        assert channel_details(Benjamin['token'], channel_id1['channel_id'])

def test_invalid_token():
    _, _, _, _, channel_id1 = initialisation()
    #Token parsed in is invalid
    #This should throw AccessError
    with pytest.raises(error.AccessError):
        assert channel_details("Booooop", channel_id1['channel_id'])
