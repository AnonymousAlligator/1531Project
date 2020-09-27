'''
Query String returns the collection of messages 
'''

from channel import channel_invite
from channels import channels_create
from auth import auth_register
from message import message_send
from other import search
import error
import pytest

Jeffo = auth_register("JeffoD@email.com", "a1b2c3", "Jeffo", "Jeff")
channels_create(Jeffo['token'], "Main Channel", True)
channel_invite(Jeffo['token'], 0, 0)
message1 = "Let's geddit"
message_send(Jeffo['token'], 0, message1)
message2 = "Shut up rat"
message_send(Jeffo['token'], 0, message2)
message3 = "Mb lmao"
message_send(Jeffo['token'], 0, message3)
message4 = "Shut up ye"
message_send(Jeffo['token'], 0, message4)


def search_onestring():
    assert search(Jeffo['token'], "Let's") == "Let's geddit"    

def search_multiplestring():
    assert search(Jeffo['token'], "Shut") == "Shut up rat", "Shut up ye"

