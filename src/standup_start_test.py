
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
from message import message_send
from other import clear

# check standup_start successfully sends
def standup_start_works():
    pass

# check for invalid channel id
def standup_start_invalid_channel():
    pass

# check for input error if existing standup in channel
def standup_start_existing_standup():
    pass
