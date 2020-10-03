import pytest
import error
from auth import auth_register
from channel import channel_details, channel_addowner, channel_invite, channel_join
from channels import channels_create
from test_helpers import create_one_test_user, create_two_test_users, create_three_test_users
from other import clear


################################################################################################
#Make user with user id u_id an owner of this channel

#Channel exists, token is an owner, u_id is a member, 
def test_channel_addowner_sucess():
    clear()
    user_0, user_1 = create_two_test_users() 
    public_channel = channels_create(user_0['token'], "name", True) #returns channel ID_0
    channel_join(user_1['token'], public_channel) 
    assert channel_addowner(user_0['token'], public_channel, user_1['u_id']) == {}

#Channel exists, token is NOT an owner, u_id is a member
def test_channel_addowner_not_owner():
    clear()
    user_0, user_1, user_2 = create_three_test_users() 
    public_channel = channels_create(user_0['token'], "name", True)
    channel_join(user_1['token'], public_channel) 
    channel_join(user_1['token'], public_channel) 
    with pytest.raises(error.AccessError):
        assert channel_addowner(user_1['token'], public_channel, user_2['u_id']) == {}

#Channel exists, token is NOT a member, u_id is a member
def test_adder_not_member():
    clear()
    user_0, user_1, user_2 = create_three_test_users() 
    public_channel = channels_create(user_0['token'], "name", True)
    channel_join(user_2['token'], public_channel) 
    with pytest.raises(error.AccessError):
        assert channel_addowner(user_1['token'], public_channel, user_2['u_id']) == {}

#Channel exists, token is owner adding someone who is already a owner
def test_channel_addowner_already_owner():
    clear()
    user_0, user_1, user_2 = create_three_test_users() 
    public_channel = channels_create(user_0['token'], "name", True)
    channel_join(user_2['token'], public_channel) 
    with pytest.raises(error.InputError):
        assert channel_addowner(user_0['token'], public_channel, user_1['u_id'])
        assert channel_addowner(user_0['token'], public_channel, user_1['u_id'])   


#Channel exists, token is adding themselves.
def test_channel_addowner_self():
    clear()
    user_0 = create_one_test_user() 
    public_channel = channels_create(user_0['token'], "name", True)
    with pytest.raises(error.InputError):
        assert channel_addowner(user_0['token'], public_channel, user_0['u_id']) == {}

#Channel does NOT exist, throw input error
def test_channel_addowner_invalid_channel(): 
    clear()
    user_0, user_1 = create_two_test_users() 
    public_channel = 4
    with pytest.raises(error.InputError):
        assert channel_addowner(user_0['token'], public_channel, user_1['u_id']) == {}

#Channel is private, user is part of private channel 
def test_channel_addowner_invited():
    clear()
    user_0, user_1 = create_two_test_users() 
    private_channel = channels_create(user_0['token'], "name", False)
    channel_invite(user_0['token'], private_channel, user_1['u_id'])
    assert channel_addowner(user_0['token'], private_channel, user_1['u_id']) == {}

#Channel is private, user is not part of private channel
def test_channel_addowner_not_invited():
    clear()
    user_0, user_1 = create_two_test_users() 
    private_channel = channels_create(user_0['token'], "name", False)
    with pytest.raises(error.InputError):
        assert channel_addowner(user_0['token'], private_channel, user_1['u_id']) == {}
