'''
Given a query string, return a collection of messages in all of the channels that the user has joined that match the query
'''

from channel import channel_invite
from channels import channels_create
from auth import auth_register
from message import message_send
from test_helpers import create_one_test_user
from error import AccessError, InputError
from other import clear, search
import pytest

@pytest.mark.skip(reason='function implementation not done yet')
# check search for existing string
def test_search_single():
    
    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates test channel
    channels_create(test_user0['token'], "Main Channel", True)
    
    # test_user0 sends message to test channel
    message_send(test_user0['token'], 0, "Let's geddit")

    assert search(test_user0['token'], "Let's") == "Let's geddit"    

@pytest.mark.skip(reason='function implementation not done yet')
# check for returning multiple strings
def test_search_multiple():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates test channel
    channels_create(test_user0['token'], "Main Channel", True)
    
    # test_user0 sends 2 messages to test channel
    message_send(test_user0['token'], 0, "Let's geddit")
    message_send(test_user0['token'], 0, "Let's go")

    assert search(test_user0['token'], "Let's") == "Let's geddit", "Let's go"

@pytest.mark.skip(reason='function implementation not done yet')
# check for string that doesn't exist
def test_search_multiplestring():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates test channel
    channels_create(test_user0['token'], "Main Channel", True)
    
    # test_user0 sends 2 messages to test channel
    message_send(test_user0['token'], 0, "Let's geddit")
    message_send(test_user0['token'], 0, "Let's go")

    assert search(test_user0['token'], "ahahhaaha") == {}

