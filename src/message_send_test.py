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


message1 = "hi"
message2 = ""
message_empty = ""
chars = 200

for i in range(chars):
    msg_char = "hello"
    message2 += msg_char

message3 = ""
chars = 201

for i in range(chars):
    msg_char = "hello"
    message3 += msg_char

@pytest.mark.skip(reason='function implementation not done yet')    
def test_message_send_lessthan1000chars_existinguser():
    clear()
    test_user_0 = create_one_test_user()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    #assert message_send(test_user_0['token'], 0, message1) == 0 #TODO: update in iter2
    assert message_send(test_user_0['token'], channel_name1, message1) == {}

@pytest.mark.skip(reason='function implementation not done yet')
def test_message_send_exactly1000chars():
    clear()
    test_user_0 = create_one_test_user()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    #assert message_send(test_user_0['token'], 0, message2) == 1 #TODO: update in iter2
    assert message_send(test_user_0['token'], channel_name1, message2) == {}

@pytest.mark.skip(reason='function implementation not done yet')
def test_message_send_message_empty():
    clear()
    test_user_0 = create_one_test_user()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    with pytest.raises(error.InputError):
       assert message_send(test_user_0['token'], channel_name1, message_empty)

@pytest.mark.skip(reason='function implementation not done yet')  
def test_message_send_morethan1000chars():
    clear()
    test_user_0 = create_one_test_user()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    with pytest.raises(error.InputError):
       assert message_send(test_user_0['token'], channel_name1, message3)
    
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

@pytest.mark.skip(reason='function implementation not done yet')  
def test_message_send_usernotinchannel():
    clear()
    test_user_0 = create_one_test_user()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    with pytest.raises(error.InputError):
       assert message_send(test_user_0['token'], channel_name1, message1)


#assume that message is a string, assume that channel given is valid, assume user is authorised
