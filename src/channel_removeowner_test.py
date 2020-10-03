import pytest
import error
from auth import auth_register
from channel import channel_details, channel_addowner, channel_invite, channel_join, channel_leave, channel_removeowner
from channels import channels_create


#Setting up data files:
#user_0 is flockowner
#Users 1, 2, 3 are part of a public channel
#User 4 is not part of any channel
#User 5 is owner of a private channel
#User 6 is a member of a private channel
user_0 = auth_register("apples@email.com", "applepass", "apple", "red") #returns { u_id, token }
user_1 = auth_register("banana@email.com", "bananapass", "banana", "yellow") #returns { u_id, token }
user_2 = auth_register("carrot@email.com", "carrotpass", "carrot", "orange") #returns { u_id, token }
user_3 = auth_register("durian@email.com", "durianpass", "durian", "yellow")
user_4 = auth_register("eggplant@email.com", "eggplantpass", "eggplant", "purple")
user_5 = auth_register("figs@email.com", "figspass", "figs", "green")
user_6 = auth_register("grape@email.com", "grapepass", "grape", "green")


#Create first public channel 
channel_0 = channels_create(user_0['token'], "name", True) #returns channel ID_0

#Users 1, 2 ,3 are part of a public channel
channel_invite(user_0['token'], channel_0, user_1['u_id'])
channel_invite(user_0['token'], channel_0, user_2['u_id'])
channel_invite(user_0['token'], channel_0, user_3['u_id'])
channel_invite(user_0['token'], channel_0, user_4['u_id'])
channel_invite(user_0['token'], channel_0, user_5['u_id'])

channel_addowner(user_0['token'], channel_0, user_1['u_id'])
channel_addowner(user_0['token'], channel_0, user_2['u_id'])

#Creating second public channel
channel_1 = channels_create(user_1['token'], "Multiple owner", True) #returns channel ID_0
channel_join(user_2['token'], channel_1)
channel_addowner(user_1['token'], channel_1, user_2['u_id'])

#Creating third public channel
channel_3 = channels_create(user_1['token'], "Single owner,two mem", True) #returns channel ID_0
channel_join(user_2['token'], channel_1)

#Creating fourth public channel
channel_4 = channels_create(user_1['token'], "Single owner,two mem", True) #returns channel ID_0

#data files for private channel checks
channel_2 = channels_create(user_1['token'], "name", False) #returns channel ID_0
channel_invite(user_1['token'], channel_2, user_2['u_id'])
channel_addowner(user_1['token'], channel_2, user_2['u_id'])

#data files for private channel checks
channel_5 = channels_create(user_0['token'], "name", False) #returns channel ID_0
########################################################################################
def test_channel_removeowner_success():
    token = user_0['token']
    u_id = user_1['u_id']
    channel_id = channel_0
    assert channel_removeowner(token, channel_id, u_id) == {}   

#Channel does not exist
def test_channel_removeowner_invalid_channel():
    token = user_0['token']
    u_id = user_2['u_id']
    channel_id = None
    with pytest.raises(error.InputError):
        assert channel_removeowner(token, channel_id, u_id) == {}    

#attempting to remove owner when the caller is not an owner
def test_channel_removeowner_caller_not_owner():
    token = user_3['token']
    u_id = user_2['u_id']
    channel_id = channel_0
    with pytest.raises(error.AccessError):
        assert channel_removeowner(token, channel_id, u_id) == {}   

#attempting to remove owner when the person called is not an owner
def test_channel_removeowner_not_owner():
    token = user_0['token']
    u_id = user_3['u_id']
    channel_id = channel_0
    with pytest.raises(error.InputError):
        assert channel_removeowner(token, channel_id, u_id) == {}   

#attempting to remove owner when neither caller or person called is owner
def test_channel_removeowner_niether_owner():
    token = user_3['token']
    u_id = user_4['u_id']
    channel_id = channel_0
    with pytest.raises(error.AccessError):
        assert channel_removeowner(token, channel_id, u_id) == {}   

#Owner removing themselves success
def test_channel_removeowner_owner_success():
    token = user_1['token']
    u_id = user_1['u_id']
    channel_id = channel_1    
    assert channel_removeowner(token, channel_id, u_id) == {}    

#Owner removing themselves as owner when there is no other owner
def test_channel_removeowner_only_owner():
    token = user_1['token']
    u_id = user_1['u_id']
    channel_id = channel_3    
    with pytest.raises(error.InputError):
        assert channel_removeowner(token, channel_id, u_id) == {}   


#Owner removing themselves as owner when there is no other member in the channel
def test_channel_removeowner_only_member():
    token = user_1['token']
    u_id = user_1['u_id']
    channel_id = channel_4
    with pytest.raises(error.InputError):
        assert channel_removeowner(token, channel_id, u_id) == {}   

#Attempting to remove owner when person is part of private channel (channel_1)
def test_channel_removeowner_invited():
    token = user_1['token']
    u_id = user_2['u_id']
    channel_id = channel_2
    assert channel_removeowner(token, channel_id, u_id) == {}

#attempting to remove owner when person is NOT part of private channel(channel_1)
def test_channel_removeowner_not_invited():
    token = user_0['token']
    u_id = user_3['u_id']
    channel_id = channel_5
    with pytest.raises(error.InputError):
        assert channel_removeowner(token, channel_id, u_id) == {}
 

