'''
AccessError when message_id was not sent by the user or when the user is not owner of the channel
'''

from channel import channel_invite, channel_addowner
from channels import channels_create
from auth import auth_register
from message import message_send, message_edit, message_remove
import error
import pytest

Jeffo = auth_register("Jeffo@email.com", "a1b2c3", "Jeffo", "Jeff")
Smith = auth_register("smith@email.com", "a1b2c3", "Smith", "Smith")
Tom = auth_register("tom@email.com", "a1b2c3", "Tom", "Tommery")

channels_create(Jeffo['token'], "Main Channel", True)
channel_invite(Jeffo['token'], 0, 0)
channel_invite(Smith['token'], 0, 1)
channel_invite(Tom['token'], 0, 2)
channel_addowner(Jeffo['token'], 0, 0)

message1 = "Let's geddit"
message_send(Jeffo['token'], 0, message1)
message2 = "Shut up rat"
message_send(Smith['token'], 0, message2)
message3 = "Mb lmao"
message_send(Jeffo['token'], 0, message3)
message4 = "I hate you"
message_send(Jeffo['token'], 0, message4)
message5 = "I love you"
message6 = "Hi"
message7 = "Rats"
def test_message_edit():
    assert message_remove(Jeffo['token'], 3, message5) == {}

def test_message_edit_notusermsg():
    with pytest.raises(error.AccessError):
        assert message_edit(Smith['token'], 0, message6)

def test_message_edit_notowner():
    message_edit(Smith['token'], 1, message6)
    with pytest.raises(error.AccessError):
        assert message_edit(Tom['token'], 0, message7) 

#assume that edited message is a string, message_id is valid