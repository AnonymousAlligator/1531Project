
'''
InputError when any of: 
Channel ID is not a valid channel, Message is more than 1000 characters, An active standup is not currently running in this channel
AccessError when the authorised user is not a member of the channel that the message is within
'''
import error
import pytest
from channel import channel_join
from channels import channels_create
from test_helpers import create_one_test_user, create_two_test_users
from standup import standup_send, standup_start
from other import clear
from time import sleep

# check standup_send successfully sends
def test_standup_send_works():
    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel0 = channels_create(test_user0['token'], "Public Channel", True)

    # test_user0 starts a standup
    standup_start(test_user0['token'], channel0['channel_id'], 2)

    #test_user0 sends message into standup
    standup_send(test_user0['token'], channel0['channel_id'], 'hi')



# check for input error when more than 1000 character message
def test_standup_send_too_long():
    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel0 = channels_create(test_user0['token'], "Public Channel", True)

    # test_user0 starts a standup
    standup_start(test_user0['token'], channel0['channel_id'], 2)

    #test_user0 tries to send message with 1001 into standup
    with pytest.raises(error.InputError):
        standup_send(test_user0['token'], channel0['channel_id'], 'a' * 1001)

# check for input error when invalid channel id
def test_standup_send_invalid_channel():
    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel0 = channels_create(test_user0['token'], "Public Channel", True)

    # test_user0 starts a standup
    standup_start(test_user0['token'], channel0['channel_id'], 2)

    #test_user0 sends standup message into invalid channel
    with pytest.raises(error.InputError):
        standup_send(test_user0['token'], channel0['channel_id'] + 1, 'hi')

# check for input error when inactive standup in channel
def test_standup_send_invalid_active():
    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel0 = channels_create(test_user0['token'], "Public Channel", True)

    # test_user0 starts a standup
    standup_start(test_user0['token'], channel0['channel_id'], 1)

    sleep(1)

    #test_user0 sends message into inactive standup
    with pytest.raises(error.InputError):
        standup_send(test_user0['token'], channel0['channel_id'], 'hi')

# check for invalid action trying to start standup during active standup
def test_standup_send_invalid_standup_start():
    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel0 = channels_create(test_user0['token'], "Public Channel", True)

    # test_user0 starts a standup
    standup_start(test_user0['token'], channel0['channel_id'], 2)

    #test_user0 tries to start standup during active standup
    with pytest.raises(error.InputError):
        standup_send(test_user0['token'], channel0['channel_id'], '/standup 1')

# check for access error when user is not channel member
def test_standup_send_invalid_user():
    clear()
    test_user0, test_user1 = create_two_test_users()

    # test_user0 creates 1 public channel
    channel0 = channels_create(test_user0['token'], "Public Channel", True)

    # test_user0 starts a standup
    standup_start(test_user0['token'], channel0['channel_id'], 2)

    #test_user1 tries to send message into standup in channel he is not part of
    with pytest.raises(error.AccessError):
        standup_send(test_user1['token'], channel0['channel_id'], 'hi')