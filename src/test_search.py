'''
Query String returns the collection of messages 
'''

from channel import channel_invite, channel_addowner
from channels import channels_create
from auth import auth_register
from message import message_send, message_remove
import error
import pytest

Dylan = auth_register("JeffoD@email.com", "a1b2c3", "Dylan", "Jeff")
channels_create(Dylan['token'], "Main Channel", True)
channel_invite(Dylan['token'], 0, 0)
message1 = "Let's geddit"
message_send(Dylan['token'], 0, message1)
message2 = "Shut up rat"
message_send(Dylan['token'], 0, message2)
message3 = "Mb lmao"
message_send(Dylan['token'], 0, message3)
message4 = "Shut up ye"
message_send(Dylan['token'], 0, message4)

def search_emptystring():
    assert search(Dylan['token'], "") == ""

def search_onestring():
    assert search(Dylan['token'], "Let's") == "Let's geddit"    

def search_multiplestring():
    assert search(Dylan['token'], "Shut") == "Shut up rat", "Shut up ye"

