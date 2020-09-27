import pytest
import error
from auth import auth_register
from channel import channel_details, channel_addowner, channel_invite
from channels import channels_create


#Setting up data files:

User_0 = auth_register("apples@email.com", "applepass", "apple", "red") gives { u_id, token }
User_1 = auth_register("banana@email.com", "bananapass", "banana", "yellow") gives { u_id, token }
User_2 auth_register("carrot@email.com", "carrotpass", "carrot", "orange") gives { u_id, token }

#create channel to join 
channel_0 = channels_create(user_0['token'], channel_0, true) #returns channel ID_0
channel_1 = channels_create(user_0['token'], channel_0, False) #returns channel ID_1

#Details owner of channel
channel_details_0 = channel_details(User_2['token'],channel_0)) #returns {name,owner_,members, all_members}

################################################################################################
#Make user with user id u_id an owner of this channel

def test_channel_addowner_sucess():
	token = User_0['token']
	u_id = User_0['u_id']
	channel_id = channel_0
	assert channel_addowner(token, channel_id, u_id)) == {}
	

def test_channel_addowner_invalid_channel(): #channel does not exist, troow input error
	token = User_0['token']
	u_id = User_0['u_id']
	channel_id = channel_2
	with pytest.raises(error.InputError):
		assert channel_addowner(token, channel_id, u_id)

def test_channel_addowner_already_owner(): #owner already owner, throw input error
	token = User_2['token']
	u_id = User_2['u_id']
	channel_id = channel_0
	with pytest.raises(error.InputError):
		assert channel_addowner(token, channel_id, u_id)



'''
def test_channel_join_inval
with pytest.raises(error.InputError):
InputError when any of:
Channel ID is not a valid channel
When user with user id u_id is already an owner of the channel

AccessError when the authorised user is not an owner of the flockr, or an owner of this channel

'''
