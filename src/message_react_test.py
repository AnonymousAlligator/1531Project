from channel import channel_join
from channels import channels_create
from message import message_send, message_react
from test_helpers import create_one_test_user, create_two_test_users
from error import InputError, AccessError
from other import clear, data
import pytest

# Check that react passes
def test_message_react():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel_id = channels_create(test_user0['token'], "Public Channel", True)
        
    # test_user0 sends 1 message to public channel
    message0 = "inital message"
    message0_id = message_send(test_user0['token'], channel_id['channel_id'], message0)

    message_react(test_user0['token'], message0_id['message_id'], 1) == {}

# Check that fails for invalid react_id
def test_message_react_invalid_reactid(): 
    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel_id = channels_create(test_user0['token'], "Public Channel", True)
        
    # test_user0 sends 1 message to public channel
    message0 = "inital message"
    message0_id = message_send(test_user0['token'], channel_id['channel_id'], message0)

    with pytest.raises(InputError):
        assert message_react(test_user0['token'], message0_id['message_id'], 5)

# Check that fails for invalid token
def test_message_react_invalid_token(): 
    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel_id = channels_create(test_user0['token'], "Public Channel", True)
        
    # test_user0 sends 1 message to public channel
    message0 = "inital message"
    message0_id = message_send(test_user0['token'], channel_id['channel_id'], message0)

    with pytest.raises(AccessError):
        assert message_react('invalid_token', message0_id['message_id'], 1)

# Check that fails for invalid message_id
def test_message_react_invalid_msg_id(): 
    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel_id = channels_create(test_user0['token'], "Public Channel", True)
        
    # test_user0 sends 1 message to public channel
    message0 = "inital message"
    message_send(test_user0['token'], channel_id['channel_id'], message0)

    with pytest.raises(InputError):
        assert message_react(test_user0['token'], 2, 1)
