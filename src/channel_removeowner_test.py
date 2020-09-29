import error
import pytest
import error
from auth import auth_register
from channel import channel_details, channel_addowner, channel_invite, channel_removeowner
from channels import channels_create


#Setting up data files:
user_0 = auth_register("apples@email.com", "applepass", "apple", "red") #returns { u_id, token }
user_1 = auth_register("banana@email.com", "bananapass", "banana", "yellow") #returns { u_id, token }
user_2 = auth_register("carrot@email.com", "carrotpass", "carrot", "orange") #returns { u_id, token }

#create channel to join 
channel_0 = channels_create(user_0['token'], "name", True) #returns channel ID_0
channel_1 = channels_create(user_0['token'], "name", False) #returns channel ID_1

#invites user_0 to the private channel
channel_invite(user_0['token'],channel_1)

#makes user_0 channel owner of public
channel_addowner(user_0['token'], channel_0, user_0['u_id'])

#Details owner of channel
channel_details_0 = channel_details(user_2['token'],channel_0) #returns {name,owner_,members, all_members}
########################################################################################

def channel_removeowner_invalid_channel():
    token = user_0['token']
    u_id = user_0['u_id']
    channel_id = None
    with pytest.raises(error.InputError):
        assert channel_removeowner(token, channel_id, u_id) == {}    

#attempting to remove owner when user id is not an owner
def channel_removeowner_not_owner():
    token = user_1['token']
    u_id = user_1['u_id']
    channel_id = channel_0
    with pytest.raises(error.InputError):
        assert channel_removeowner(token, channel_id, u_id) == {}   

#attempting to remove owner when they are part of private channel (channel_1)
def channel_removeowner_invited
    token = user_0['token']
    u_id = user_0['u_id']
    channel_id = channel_1
    assert channel_removeowner(token, channel_id, u_id) == {}

#attempting to remove owner when they are NOT part of private channel(channel_1)
def test_channel_addowner_not_invited
    token = user_1['token']
    u_id = user_1['u_id']
    channel_id = channel_1
    with pytest.raises(error.AccessError):
        assert channel_addowner(token, channel_id, u_id) == {}
 


'''
Remove user with user id u_id an owner of this channel

InputError when any of:
Channel ID is not a valid channel
When user with user id u_id is not an owner of the channel

AccessError when the authorised user is not an owner of the flockr, or an owner of this channel
'''