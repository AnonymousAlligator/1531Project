from channel import channel_join, channel_leave
from channels import channels_create
from message import message_send, message_pin, message_unpin
from test_helpers import create_one_test_user, create_two_test_users
from error import InputError, AccessError
from other import clear
import pytest

# Check that pinning a message works
def test_message_unpin():
    
    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel_id = channels_create(test_user0['token'], "Public Channel", True)
        
    # test_user0 sends 1 message to public channel
    message0 = "inital message"
    message0_id = message_send(test_user0['token'], channel_id['channel_id'], message0)
    message_pin(test_user0['token'], message0_id['message_id'])

    assert message_unpin(test_user0['token'], message0_id['message_id']) == {}

# Check that unpinning while not in the channel raises error
def test_message_unpin_notmember():
    
    clear()
    test_user0, test_user1 = create_two_test_users()

    # test_user0 creates 1 public channel
    channel_id = channels_create(test_user1['token'], "Public Channel", True)
        
    # test_user1 sends 1 message to public channel
    message1 = "inital message"
    message1_id = message_send(test_user1['token'], channel_id['channel_id'], message1)
    channel_join(test_user0['token'], channel_id['channel_id'])
    message_pin(test_user0['token'], message1_id['message_id'])
    channel_leave(test_user0['token'], channel_id['channel_id'])
    
    with pytest.raises(AccessError):
        message_unpin(test_user0['token'], message1_id['message_id'])

# Check that only owners can pin
def test_message_unpin_owner():

    clear()
    test_user0, test_user1 = create_two_test_users()

    # test_user0 creates 1 public channel
    channel_id = channels_create(test_user0['token'], "Main Channel", True)

    # test_user1 joins public channel 
    channel_join(test_user1['token'], channel_id['channel_id'])
        
    # test_user0 sends 1 message
    message0 = "initial message"
    message0_id = message_send(test_user0['token'], channel_id['channel_id'], message0)
    message_pin(test_user0['token'], message0_id['message_id'])

    # raise error if user1 tries to unpin user0's message
    with pytest.raises(AccessError):
        message_unpin(test_user1['token'], message0_id['message_id'])

def test_message_unpin_invalidmsgid():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel_id = channels_create(test_user0['token'], "Public Channel", True)
        
    # test_user0 sends 1 message to public channel
    message0 = "inital message"
    message0_id = message_send(test_user0['token'], channel_id['channel_id'], message0)
    message_pin(test_user0['token'], message0_id['message_id'])

    with pytest.raises(InputError):
        message_unpin(test_user0['token'], 2)

def test_message_pin_alreadyunpinned():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel_id = channels_create(test_user0['token'], "Public Channel", True)
        
    # test_user0 sends 1 message to public channel
    message0 = "inital message"
    message0_id = message_send(test_user0['token'], channel_id['channel_id'], message0)
    message_pin(test_user0['token'], message0_id['message_id'])
    message_unpin(test_user0['token'], message0_id['message_id'])

    with pytest.raises(InputError):
        message_unpin(test_user0['token'], message0_id['message_id'])

def test_message_pin_invalidtoken():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel_id = channels_create(test_user0['token'], "Public Channel", True)
        
    # test_user0 sends 1 message to public channel
    message0 = "inital message"
    message0_id = message_send(test_user0['token'], channel_id['channel_id'], message0)
    message_pin(test_user0['token'], message0_id['message_id'])

    # raise error if user1 tries to pin user0's message
    with pytest.raises(AccessError):
        message_unpin('hello', message0_id['message_id'])