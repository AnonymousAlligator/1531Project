from channel import channel_join
from channels import channels_create
from test_helpers import create_one_test_user, create_two_test_users
from message import message_sendlater, message_send
from other import clear
from datetime import datetime
import error
import pytest
from time import sleep
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
    
message_spaces = ""
message_spaces += " "*100


#Checking message ID's are sent in assigned in order
def test_message_sendlater_in_order():
    clear()
    test_user_0, test_user_1 = create_two_test_users()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    channel_join(test_user_1['token'],channel_name1['channel_id'])
    message_sendlater(test_user_1['token'], channel_name1['channel_id'], message1, (datetime.now()).timestamp()+2)
    message_send(test_user_1['token'], channel_name1['channel_id'], message1)
    message_send(test_user_0['token'], channel_name1['channel_id'], message1)
    message_sendlater(test_user_0['token'], channel_name1['channel_id'], message1, (datetime.now()).timestamp()+4)
    sleep(2.5)
    assert message_send(test_user_1['token'], channel_name1['channel_id'], message1) == {'message_id': 3}
    sleep(2.5)
    assert message_send(test_user_1['token'], channel_name1['channel_id'], message1) == {'message_id': 5}

#Successfully sending message less than 1000 characters
def test_message_sendlater_lessthan1000chars():
    clear()
    test_user_0 = create_one_test_user()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    message_sendlater(test_user_0['token'], channel_name1['channel_id'], message1, (datetime.now()).timestamp()+1)
    sleep(1.5)
    assert message_send(test_user_0['token'], channel_name1['channel_id'], message1) == {'message_id': 1}

#Successfully sending message exactly 1000 characters
def test_message_sendlater_exactly1000chars():
    clear()
    test_user_0 = create_one_test_user()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    message_sendlater(test_user_0['token'], channel_name1['channel_id'], message2, (datetime.now()).timestamp()+1)
    sleep(1.5)
    assert message_send(test_user_0['token'], channel_name1['channel_id'], message2) == {'message_id': 1}

#Attempting to send an empty message
def test_message_sendlater_message_empty():
    clear()
    test_user_0 = create_one_test_user()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    with pytest.raises(error.InputError):
       message_sendlater(test_user_0['token'], channel_name1['channel_id'], message_empty, (datetime.now()).timestamp()+1)

#Attempting to send a message with only spaces
def test_message_sendlater_message_spaces():
    clear()
    test_user_0 = create_one_test_user()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    with pytest.raises(error.InputError):
        assert message_sendlater(test_user_0['token'], channel_name1['channel_id'], message_spaces, (datetime.now()).timestamp()+1)

#Attempting to send a message with over 1000 characters
def test_message_sendlater_morethan1000chars():
    clear()
    test_user_0 = create_one_test_user()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    with pytest.raises(error.InputError):
        assert message_sendlater(test_user_0['token'], channel_name1['channel_id'], message3, (datetime.now()).timestamp()+1)

#Attempting to send a message when the user is not in the channel
def test_message_sendlater_usernotinchannel():
    clear()
    test_user_0, test_user_1 = create_two_test_users()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    with pytest.raises(error.AccessError):
        message_sendlater(test_user_1['token'], channel_name1['channel_id'], message1, (datetime.now()).timestamp()+1)

#Attempting to send a invalide channel
def test_message_sendlater_invalid_ch():
    clear()
    test_user_0 = create_one_test_user()
    channels_create(test_user_0['token'], "Main Channel", True)
    with pytest.raises(error.InputError):
        message_sendlater(test_user_0['token'], 3, message1, (datetime.now()).timestamp()+1)

#Attempting to send invalid token
def test_message_sendlater_invalid_token():
    clear()
    test_user_0 = create_one_test_user()
    channel_name1 = channels_create(test_user_0['token'], "Main Channel", True)
    with pytest.raises(error.AccessError):
        message_sendlater('boop', channel_name1['channel_id'], message1, (datetime.now()).timestamp()+1)