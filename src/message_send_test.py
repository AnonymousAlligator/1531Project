'''
InputError when channel name is more than 1000 characters
AccessError when the user has not joined the channel
'''

from channel import channel_invite, channel_join
from channels import channels_create
from auth import auth_register
from test_helpers import create_one_test_user, create_two_test_users, create_three_test_users
from message import message_send
from other import clear

import error
import pytest
########################################
#Creating messages
message1 = "hi"
message_empty = ""

#Creating message with 1000 characters
chars = 200
message2 = ""
for i in range(chars):
    msg_char = "hello"
    message2 += msg_char

#Creating message with 1001 characters
message3 = ""
chars = 201
for i in range(chars):
    msg_char = "hello"
    message3 += msg_char

message_spaces += " "*100


#Checking message ID's are sent in assigned in order
@pytest.mark.skip(reason='function implementation not done yet')
def test_message_send_in_order():
    clear()
    test_user_0, test_user_1 = create_two_test_users()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    channel_join(test_user_1['token'],channel_name1)
    #TODO: update in iter2
    #assert message_send(test_user_1['token'], channel_name1, message1) == 0
    assert message_send(test_user_1['token'], channel_name1, message1) == {}
    #assert message_send(test_user_1['token'], channel_name1, message1) == 1
    assert message_send(test_user_1['token'], channel_name1, message1) == {}
    #assert message_send(test_user_0['token'], channel_name1, message1) == 2
    assert message_send(test_user_0['token'], channel_name1, message1) == {}

#Successfully sending message less than 1000 characters
@pytest.mark.skip(reason='function implementation not done yet')
def test_message_send_lessthan1000chars_existinguser():
    clear()
    test_user_0 = create_one_test_user()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    #assert message_send(test_user_0['token'], 0, message1) == 0 #TODO: update in iter2
    assert message_send(test_user_0['token'], channel_name1, message1) == {}

#Successfully sending message exactly 1000 characters
@pytest.mark.skip(reason='function implementation not done yet')
def test_message_send_exactly1000chars():
    clear()
    test_user_0 = create_one_test_user()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    #assert message_send(test_user_0['token'], 0, message2) == 1 #TODO: update in iter2
    assert message_send(test_user_0['token'], channel_name1, message2) == {}

#Attempting to send an empty message
@pytest.mark.skip(reason='function implementation not done yet')
def test_message_send_message_empty():
    clear()
    test_user_0 = create_one_test_user()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    with pytest.raises(error.InputError):
       assert message_send(test_user_0['token'], channel_name1, message_empty)

#Attempting to send a message with only spaces
@pytest.mark.skip(reason='function implementation not done yet')
def test_message_send_message_spaces():
    clear()
    test_user_0 = create_one_test_user()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    with pytest.raises(error.InputError):
       assert message_send(test_user_0['token'], channel_name1, message_spaces)

#Attempting to send a message with over 1000 characters
@pytest.mark.skip(reason='function implementation not done yet')
def test_message_send_morethan1000chars():
    clear()
    test_user_0 = create_one_test_user()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    with pytest.raises(error.InputError):
       assert message_send(test_user_0['token'], channel_name1, message3)


#Attempting to send a message when the user is not in the channel
@pytest.mark.skip(reason='function implementation not done yet')
def test_message_send_usernotinchannel():
    clear()
    test_user_0 = create_one_test_user()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    with pytest.raises(error.AccessError):
       assert message_send(test_user_0['token'], channel_name1, message1)


