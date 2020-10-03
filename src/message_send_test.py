'''
InputError when channel name is more than 1000 characters
AccessError when the user has not joined the channel
'''

from channel import channel_invite, channel_join
from channels import channels_create
from auth import auth_register
from message import message_send
import error
import pytest

Jeffo = auth_register("Jeffo@email.com", "a1b2c3", "Jeffo", "Jeff")
Smith = auth_register("smith@email.com", "a1b2c3", "Smith", "Smith")
John = auth_register("john@email.com", "a1b2c3", "John", "Johno")

channel_name1 = channels_create(Jeffo['token'], "Main Channel", True)
channel_join(John['token'],0)

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

    
def test_message_send_lessthan1000chars_existinguser():
    assert message_send(Jeffo['token'], 0, message1) == 0

def test_message_send_exactly1000chars():
    assert message_send(Jeffo['token'], 0, message2) == 1
    
def test_message_send_message_empty():
    with pytest.raises(error.InputError):
        assert message_send(Jeffo['token'], 0, message_empty)

def test_message_send_morethan1000chars():
    with pytest.raises(error.InputError):
        assert message_send(Jeffo['token'], 0, message3)

def test_message_send_by_member_sucess():
    assert message_send(John['token'], 0, message1) == 3

def test_second_message_send_by_member_sucess():
    assert message_send(John['token'], 0, message1) == 4

def test_third_message_send_by_owner_sucess():
    assert message_send(Jeffo['token'], 0, message1) == 5    

def test_message_send_usernotinchannel():
    with pytest.raises(error.InputError):
        assert message_send(Smith['token'], 0, message1)



#assume that message is a string, assume that channel given is valid, assume user is authorised
