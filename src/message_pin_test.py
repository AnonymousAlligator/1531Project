from channel import channel_join
from channels import channels_create
from message import message_send, message_pin
from test_helpers import create_one_test_user, create_two_test_users
from error import InputError, AccessError
from other import clear
import pytest

# Check that pinning a message works
def test_message_pin():
    
    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel_id = channels_create(test_user0['token'], "Public Channel", True)
        
    # test_user0 sends 1 message to public channel
    message0 = "inital message"
    message0_id = message_send(test_user0['token'], channel_id['channel_id'], message0)

    assert message_pin(test_user0['token'], message0_id['message_id']) == {}

# Check that pinning while not in the channel raises error
def test_message_pin_notmember():
    
    clear()
    test_user0, test_user1 = create_two_test_users()

    # test_user0 creates 1 public channel
    channel_id = channels_create(test_user1['token'], "Public Channel", True)
        
    # test_user0 sends 1 message to public channel
    message0 = "inital message"
    message0_id = message_send(test_user1['token'], channel_id['channel_id'], message0)

    with pytest.raises(AccessError):
        message_pin(test_user0['token'], message0_id['message_id'])

# Check that only owners can pin
def test_message_pin_owner():

    clear()
    test_user0, test_user1 = create_two_test_users()

    # test_user0 creates 1 public channel
    public_channel_id = channels_create(test_user0['token'], "Main Channel", True)

    # test_user1 joins public channel 
    channel_join(test_user1['token'], public_channel_id['channel_id'])
        
    # test_user0 sends 1 message
    message0 = "user0's message"
    message0_id = message_send(test_user0['token'], public_channel_id['channel_id'], message0)

    # raise error if user1 tries to pin user0's message
    with pytest.raises(AccessError):
        message_pin(test_user1['token'], message0_id['message_id'])

def test_message_pin_invalidmsgid():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel_id = channels_create(test_user0['token'], "Public Channel", True)
        
    # test_user0 sends 1 message to public channel
    message0 = "inital message"
    message0_id = message_send(test_user0['token'], channel_id['channel_id'], message0)

    with pytest.raises(InputError):
        message_pin(test_user0['token'], 2)

def test_message_pin_alreadypinned():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel_id = channels_create(test_user0['token'], "Public Channel", True)
        
    # test_user0 sends 1 message to public channel
    message0 = "inital message"
    message0_id = message_send(test_user0['token'], channel_id['channel_id'], message0)
    message_pin(test_user0['token'], message0_id['message_id'])

    with pytest.raises(InputError):
        message_pin(test_user0['token'], message0_id['message_id'])

def test_message_pin_invalidtoken():

    clear()
    test_user0, test_user1 = create_two_test_users()

    # test_user0 creates 1 public channel
    public_channel_id = channels_create(test_user0['token'], "Main Channel", True)

    # test_user1 joins public channel 
    channel_join(test_user1['token'], public_channel_id['channel_id'])
        
    # test_user0 sends 1 message
    message0 = "user0's message"
    message0_id = message_send(test_user0['token'], public_channel_id['channel_id'], message0)

    # raise error if user1 tries to pin user0's message
    with pytest.raises(AccessError):
        message_pin('hello', message0_id['message_id'])