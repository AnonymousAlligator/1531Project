
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
from message import message_send
from other import clear

# check standup_send successfully sends
def standup_send_works():
    pass

# check for input error when more than 1000 character message
def standup_send_too_long():
    pass

# check for input error when invalid channel id
def standup_send_invalid_channel():
    pass

# check for input error when inactive standup in channel
def standup_send_invalid_active():
    pass

# check for access error when user is not channel member
def standup_send_invalid_user():
    pass