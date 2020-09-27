'''
InputError when message does not exist
AccessError when message_id was not sent by the user or when the user is not owner of the channel
'''

from channel import channel_invite, channel_addowner
from channels import channels_create
from auth import auth_register
from message import message_send, message_remove
import error
import pytest

Dylan = auth_register("Jeffo@email.com", "a1b2c3", "Dylan", "Jeff")
Smith = auth_register("smith@email.com", "a1b2c3", "Smith", "Smith")
Tom = auth_register("tom@email.com", "a1b2c3", "Tom", "Tommery")

channels_create(Dylan['token'], "Main Channel", True)
channel_invite(Dylan['token'], 0, 0)
channel_invite(Smith['token'], 0, 1)
channel_invite(Tom['token'], 0, 2)
channel_addowner(Dylan['token'], 0, 0)

message1 = "Let's geddit"
message_send(Dylan['token'], 0, message1)
message2 = "Shut up rat"
message_send(Smith['token'], 0, message2)
message3 = "Mb lmao"
message_send(Dylan['token'], 0, message3)
message4 = "I hate you"
message_send(Dylan['token'], 0, message4)
message_remove(Dylan['token'], 3)

def test_message_remove_firstmessage():
    assert message_remove(Dylan['token'], 0) == {}

def test_message_remove_ownerremove():
    assert message_remove(Dylan['token'], 1) == {}

def test_message_remove_messagenolonderexists():
    with pytest.raises(error.InputError):
        assert message_remove(Dylan['token'], 3)

def test_message_remove_messagedoesnotbelongtouser():
    with pytest.raises(error.AccessError):
        assert message_remove(Smith['token'], 0)

def test_message_remove_isnotowner():
    with pytest.raises(error.AccessError):
        assert message_remove(Tom['token'], 0)       