import pytest
import error
from auth import auth_register
from channel import channel_details, channel_addowner, channel_invite, channel_join, channel_leave, channel_removeowner
from test_helpers import create_one_test_user, create_two_test_users, create_three_test_users
from channels import channels_create
from other import clear

#Setting up data files:
#user_0 is flockowner
#Users 1, 2, 3 are part of a public channel
#User 4 is not part of any channel
#User 5 is owner of a private channel
#User 6 is a member of a private channel

########################################################################################
#Successfully removes owner
def test_channel_removeowner_success():
    clear()
    user_0, user_1 = create_two_test_users() 
    public_channel = channels_create(user_0['token'], "name", True)
    channel_join(user_1['token'], public_channel)
    channel_addowner(user_0['token'], public_channel, user_1['u_id'])
    assert channel_removeowner(user_0['token'], public_channel, user_1['u_id']) == {}   

#Successfully removed themselves as owner
def test_channel_removeowner_owner_success():
    clear()
    user_0, user_1, user_2 = create_three_test_users() 
    public_channel = channels_create(user_0['token'], "name", True)
    channel_join(user_1['token'], public_channel) 
    channel_join(user_2['token'], public_channel) 
    channel_addowner(user_0['token'], public_channel, user_1['u_id'])
    assert channel_removeowner(user_1['token'], public_channel, user_1['u_id']) == {}    

#Successfully removing owner who is part of a private channel
def test_channel_removeowner_invited():
    clear()
    user_0, user_1 = create_two_test_users() 
    private_channel = channels_create(user_0['token'], "name", False)
    channel_invite(user_0['token'], private_channel, user_1['u_id'])
    channel_addowner(user_0['token'], private_channel, user_1['u_id'])
    assert channel_removeowner(user_0['token'], private_channel, user_1['u_id']) == {}
    

#Channel does not exist
def test_channel_removeowner_invalid_channel():
    clear()
    user_0 = create_one_test_user() 
    public_channel = 4
    with pytest.raises(error.InputError):
        assert channel_removeowner(user_0['token'], public_channel, user_0['u_id']) == {}    

#Attempting to remove owner when the caller is not an owner.
def test_channel_removeowner_caller_not_owner():
    clear()
    user_0, user_1, user_2 = create_three_test_users() 
    public_channel = channels_create(user_0['token'], "name", True)
    channel_join(user_1['token'], public_channel) 
    channel_join(user_2['token'], public_channel) 
    channel_addowner(user_0['token'], public_channel, user_2['u_id'])
    with pytest.raises(error.AccessError):
        assert channel_removeowner(user_1['token'], public_channel, user_2['u_id']) == {}   

#Attempting to remove owner when the person called is not an owner.
def test_channel_removeowner_not_owner():
    clear()
    user_0, user_1, user_2 = create_three_test_users() 
    public_channel = channels_create(user_0['token'], "name", True)
    channel_join(user_1['token'], public_channel) 
    channel_join(user_2['token'], public_channel) 
    with pytest.raises(error.InputError):
        assert channel_removeowner(user_0['token'], public_channel, user_2['u_id']) == {}   

#Attempting to remove owner when neither caller or person called is owner.
def test_channel_removeowner_neither_owner():
    clear()
    user_0, user_1, user_2 = create_three_test_users() 
    public_channel = channels_create(user_0['token'], "name", True)
    channel_join(user_1['token'], public_channel) 
    channel_join(user_2['token'], public_channel) 
    with pytest.raises(error.AccessError):
        assert channel_removeowner(user_1['token'], public_channel, user_2['token']) == {}   

#Owner removing themselves as owner when there is only one owner but other members
def test_channel_removeowner_only_owner():
    clear()
    user_0, user_1 = create_two_test_users() 
    public_channel = channels_create(user_0['token'], "name", True)
    channel_join(user_1['token'], public_channel)     
    with pytest.raises(error.InputError):
        assert channel_removeowner(user_0['token'], public_channel, user_0['u_id']) == {}   


#Owner removing themselves as owner when there is no other member in the channel and they are the only owner.
def test_channel_removeowner_only_member():
    clear()
    user_0 = create_one_test_user() 
    public_channel = channels_create(user_0['token'], "name", True)   
    with pytest.raises(error.InputError):
        assert channel_removeowner(user_0['token'], public_channel, user_0['u_id']) == {}  


#Attempting to remove owner when the person called is NOT part of private channel
def test_channel_removeowner_not_invited():
    clear()
    user_0, user_1 = create_two_test_users() 
    private_channel = channels_create(user_0['token'], "name", False)
    with pytest.raises(error.InputError):
        assert channel_removeowner(user_0['token'],private_channel, user_1['u_id']) == {}
 

