'''
InputError when message does not exist
AccessError when message_id was not sent by the user or when the user is not owner of the channel
'''

from channel import channel_invite, channel_addowner
from channels import channels_create
from auth import auth_register
from message import message_send, message_remove
from test_helpers import create_three_test_users
from error import InputError
from other import clear
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
message_remove(Jeffo['token'], 3)

def test_message_remove_firstmessage():

    clear()
    test_user0, test_user1, test_user2 = create_three_test_users()

    assert message_remove(Jeffo['token'], 0) == {}

def test_message_remove_ownerremove():
    assert message_remove(Jeffo['token'], 1) == {}

def test_message_remove_messagenolonderexists():
    with pytest.raises(error.InputError):
        assert message_remove(Jeffo['token'], 3)

def test_message_remove_messagedoesnotbelongtouser():
    with pytest.raises(error.AccessError):
        assert message_remove(Smith['token'], 0)

def test_message_remove_isnotowner():
    with pytest.raises(error.AccessError):
        assert message_remove(Tom['token'], 0)