
'''
InputError when any of:
Channel ID is not a valid channel
An active standup is currently running in this channel
'''
import error
import pytest
from channel import channel_join
from channels import channels_create
from test_helpers import create_one_test_user, create_two_test_users
from standup import standup_start
from other import clear
from time import time

# check for invalid channel id
def test_standup_start_invalid_channel():
    
    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel0 = channels_create(test_user0['token'], "Public Channel", True)

    # test_user0 starts standup in invalid channel
    with pytest.raises(error.InputError):
        standup_start(test_user0['token'], channel0['channel_id'] + 1, 2)

# check for input error if existing standup in channel
def test_standup_start_existing_standup():
    
    clear()
    test_user0, test_user1 = create_two_test_users()

    # test_user0 creates 1 public channel
    channel0 = channels_create(test_user0['token'], "Public Channel", True)
    
    # test_user1 joins channel0
    channel_join(test_user1['token'], channel0['channel_id'])

    # test_user0 starts a standup
    standup_start(test_user0['token'], channel0['channel_id'], 2)

    # test_user1 also tries to starts a standup
    with pytest.raises(error.InputError):
        standup_start(test_user1['token'], channel0['channel_id'], 2)
