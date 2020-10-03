import pytest
import error
from auth import auth_register
from channel import channel_details, channel_addowner, channel_invite, channel_join
from channels import channels_create
from test_helpers import create_one_test_user, create_two_test_users
from other import clear


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


#Create public channel to join 
channel_0 = channels_create(user_0['token'], "name", True) #returns channel ID_0
#Creates private channel to join
channel_1 = channels_create(user_5['token'], "name", False) #returns channel ID_1

#Users 1, 2 ,3 are part of a public channel
channel_join(user_1['token'], channel_0)
channel_join(user_2['token'], channel_0)
channel_join(user_3['token'], channel_0)

#User 6 is a member of a private channel
channel_invite(user_5['token'], channel_1, user_6['u_id'])

################################################################################################
#Make user with user id u_id an owner of this channel

#Channel exists, token is an owner, u_id is a member, 
def test_channel_addowner_sucess():
    
    clear()
    
    token = user_0['token']
    u_id = user_1['u_id']
    channel_id = channel_0
    assert channel_addowner(token, channel_id, u_id) == {}

#Channel exists, token is NOT an owner, u_id is a member
def test_channel_addowner_not_owner():
    
    clear()
    
    token = user_3['token']
    u_id = user_2['u_id']
    channel_id = channel_0
    with pytest.raises(error.AccessError):
        assert channel_addowner(token, channel_id, u_id) == {}

#Channel exists, token is NOT a member, u_id is a member
def test_adder_not_member():
    
    clear()

    token = user_4['token']
    u_id = user_2['u_id']
    channel_id = channel_0
    with pytest.raises(error.AccessError):
        assert channel_addowner(token, channel_id, u_id) == {}

#Channel exists, token is owner adding someone who is already a owner
def test_channel_addowner_already_owner():
    
    clear()

    token = user_0['token']
    u_id = user_1['u_id']
    channel_id = channel_0
    with pytest.raises(error.InputError):
        assert channel_addowner(token, channel_id, u_id) == {}

#Channel exists, token is adding themselves.
def test_channel_addowner_self():
    
    clear()

    token = user_0['token']
    u_id = user_0['u_id']
    channel_id = channel_0
    with pytest.raises(error.InputError):
        assert channel_addowner(token, channel_id, u_id) == {}

#Channel does NOT exist, throw input error
def test_channel_addowner_invalid_channel(): 
    
    clear()

    token = user_0['token']
    u_id = user_1['u_id']
    channel_id = 4
    with pytest.raises(error.InputError):
        assert channel_addowner(token, channel_id, u_id) == {}

#Channel is private, user is part of private channel 
def test_channel_addowner_invited():
    
    clear()

    token = user_5['token']
    u_id = user_6['u_id']
    channel_id = channel_1
    assert channel_addowner(token, channel_id, u_id) == {}

#Channel is private, user is not part of private channel
def test_channel_addowner_not_invited():
    
    clear()
    
    token = user_5['token']
    u_id = user_2['u_id']
    channel_id = channel_1
    with pytest.raises(error.InputError):
        assert channel_addowner(token, channel_id, u_id) == {}
