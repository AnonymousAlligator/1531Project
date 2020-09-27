from auth import auth_register
from channel import channel_invite
from channels import channels_create
from error import InputError, AccessError
from other import clear
import pytest

def test_channel_invite():

    clear()

    zero_user = auth_register("user1@email.com", "hellothere", "Mike", "Pike")
    one_user = auth_register("user1@email.com", "overthere", "Like", "Kite")
    two_user = auth_register("user1@email.com", "somewherethere", "Rite", "Lite")

    channels_create(zero_user['token'], "Chan1", "true") #0
    channels_create(one_user['token'], "Chan2", "true") #1 
    channels_create(two_user['token'], "Chan3", "true") #2

    # test valid channels
    assert channel_invite(zero_user['token'], 0, 2) == {} # invites user 2 to channel 0
    assert channel_invite(one_user['token'], 1, 0) == {} # invites user 0 to channel 1
    assert channel_invite(two_user['token'], 2, 1) == {} # invites user 1 to channel 2

    # Test bad token
    with pytest.raises(AccessError):
        channel_invite(two_user['token'], 1, 0) 

    # Test invalid channel
    with pytest.raises(InputError):
        channel_invite(zero_user['token'], 9876, 2) 

    # Test invalid uID
    with pytest.raises(InputError):
        channel_invite(zero_user['token'], 0, 17) 

    # Test when user inviting to a channel is not part of that channel themself
    with pytest.raises(AccessError):
        channel_invite(two_user['token'], 1, 0)
    
