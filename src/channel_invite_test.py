from auth import auth_register
from channel import channel_invite, channel_join
from channels import channels_create
from error import InputError, AccessError
from test_helpers import create_one_test_user, create_two_test_users, create_three_test_users
from other import clear
import pytest



#Owner inside channel inviting user
def test_channel_invite_owner_pass():
    clear()
    user_0, user_1 = create_two_test_users()
    channel = channels_create(user_0['token'], "name", True)
    assert channel_invite(user_0['token'], channel['channel_id'], user_1['u_id']) == {}

#Member inside channel inviting user
def test_channel_invite_member_pass():
    clear()
    user_0, user_1, user_2 = create_three_test_users()
    channel = channels_create(user_0['token'], "name", True)
    channel_join(user_1['token'], channel['channel_id'])
    assert channel_invite(user_0['token'], channel['channel_id'], user_2['u_id']) == {}

# Test invalid channel
def test_channel_invite_invalid_channel():
    clear()
    user_0, user_1 = create_two_test_users()
    channel = 4
    with pytest.raises(InputError):
        assert channel_invite(user_0['token'], channel, user_1['u_id']) 

# Invitee does not exist as a user
def test_channel_invite_invalid_u_id():
    clear()
    user_0 = create_one_test_user()
    channel = channels_create(user_0['token'], "name", True)
    with pytest.raises(InputError):
        assert channel_invite(user_0['token'], channel['channel_id'], 17) 

# Inviter does not exist as a user
def test_channel_invite_invalid_caller():
    clear()
    user_0, user_1 = create_two_test_users()
    channel = channels_create(user_0['token'], "name", True)
    with pytest.raises(AccessError):
        assert channel_invite(40, channel['channel_id'], user_1['u_id']) 

#Inviter not member of channel
def test_channel_invite_inviter_not_member():
    clear()
    user_0, user_1, user_2 = create_three_test_users()
    channel = channels_create(user_0['token'], "name", True)
    with pytest.raises(AccessError):
        assert channel_invite(user_1['token'], channel['channel_id'], user_2['u_id'])

#Invited person is already an a member
def test_channel_person_already_member():
    clear()
    user_0, user_1 = create_two_test_users()
    channel = channels_create(user_0['token'], "name", True)
    channel_join(user_1['token'], channel['channel_id'])
    with pytest.raises(InputError):
        assert channel_invite(user_0['token'], channel['channel_id'], user_1['u_id'])
