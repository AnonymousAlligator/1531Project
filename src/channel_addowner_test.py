import pytest
import error
from auth import auth_register
from channel import channel_details, channel_addowner, channel_invite
from channels import channels_create


#Setting up data files:
#user_0 is flockowner
user_0 = auth_register("apples@email.com", "applepass", "apple", "red") #returns { u_id, token }
#user_1 is owner of channel
user_1 = auth_register("banana@email.com", "bananapass", "banana", "yellow") #returns { u_id, token }
#user_2 is not owner of channel
user_2 = auth_register("carrot@email.com", "carrotpass", "carrot", "orange") #returns { u_id, token }
#user_3 is not a member of the channel
user_3 = auth_register("durian@email.com", "durianpass", "durian", "yellow")
#user_4 is member of the channel (used for successes) 
user_4 = auth_register("eggplant@email.com", "eggplantpass", "eggplant", "purple")

#create public channel to join 
channel_0 = channels_create(user_0['token'], "name", True) #returns channel ID_0
#creates private channel to join
channel_1 = channels_create(user_0['token'], "name", False) #returns channel ID_1

#invites user_0 to the private channel
channel_invite(user_0['token'],channel_1)
channel_invite(user_1['token'], channel_1)

#Details owner of channel
channel_details_0 = channel_details(user_2['token'],channel_0) #returns {name,owner_,members, all_members}


################################################################################################
#Make user with user id u_id an owner of this channel

#Channel exists, public channel, token is an owner, u_id is a member, 
def test_channel_addowner_sucess():
    token = user_0['token']
    u_id = user_1['u_id']
    channel_id = channel_0
    assert channel_addowner(token, channel_id, u_id) == {}

#Channel exists, public channel, token is not an owner, u_id is a member
#Channel exists, public channel, token is an owner, u_id is not a member
#Channel exists, private channel, token not an owner, u_id is a not a member
#Channel exists, public channel, token is flock owner, uid is a member
#Channel exists, public channel, token is flock owner, uid is a member

#Channel does not exist, throw input error
def test_channel_addowner_invalid_channel(): 
    token = user_0['token']
    u_id = user_1['u_id']
    channel_id = None
    with pytest.raises(error.InputError):
        assert channel_addowner(token, channel_id, u_id) == {}
#Caller is not an owner


#Channel exists, public channel, token is owner but u_id is owner.
#NEEDS FIXING
def test_channel_addowner_already_owner():
    token = user_2['token']
    u_id = user_3['u_id']
    channel_id = channel_0
    with pytest.raises(error.InputError):
        assert channel_addowner(token, channel_id, u_id) == {}

#user 0 is part of private channel(channel_1)
def test_channel_addowner_invited():
    token = user_0['token']
    u_id = user_1['u_id']
    channel_id = channel_1
    assert channel_addowner(token, channel_id, u_id) == {}

#user 1 is NOT part of private channel(channel_1)
def test_channel_addowner_not_invited:
    token = user_1['token']
    u_id = user_1['u_id']
    channel_id = channel_1
    with pytest.raises(error.AccessError):
        assert channel_addowner(token, channel_id, u_id) == {}
