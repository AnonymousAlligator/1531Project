'''
Given a query string, return a collection of messages in all of the channels that the user has joined that match the query
'''
from channels import channels_create
from message import message_send
from test_helpers import create_two_test_users
import error
from other import clear, search
import pytest

def initialisation():
    clear()
    test_user0, test_user1 = create_two_test_users()
    #create 2 channels
    channel_id0 = channels_create(test_user0['token'], "Main Channel", True)
    channel_id1 = channels_create(test_user0['token'], "Secondary Channel", True)
    #implement messages in both channels
    message_send(test_user0['token'], 0, "Let's geddit")
    message_send(test_user0['token'], 0, "Let's go")

    expectedmessages0 = [{'message_id': 1,
                          'channel_id': 0,
                          'u_id': 0,
                          'message': "Let's go"},
                         {'message_id': 0,
                          'channel_id': 0,
                          'u_id': 0,
                          'message': "Let's geddit"},]


    message_send(test_user0['token'], 1, "Hello")
    message_send(test_user0['token'], 1, "Hi")
    message_send(test_user0['token'], 1, "Hey")

    expectedmessages1 = [{'message_id': 4,
                          'channel_id': 1,
                          'u_id': 0,
                          'message': "Hey"},
                         {'message_id': 2,
                          'channel_id': 1,
                          'u_id': 0,
                          'message': "Hello"},
                         {'message_id': 1,
                          'channel_id': 0,
                          'u_id': 0,
                          'message': "Let's go"},
                         {'message_id': 0,
                          'channel_id': 0,
                          'u_id': 0,
                          'message': "Let's geddit"}]

    return test_user0, test_user1, expectedmessages0, expectedmessages1, channel_id0, channel_id1

# check search for existing string
def test_search_single():
    user0, _, _, _ = initialisation()
    searchdict = search(user0['token'], "geddit")
    for msg in searchdict['messages']:
        assert msg['message_id'] == 0
        assert msg['channel_id'] == 0
        assert msg['u_id'] == 0
        assert msg['message'] == "Let's geddit"

# check for returning multiple strings that are not case sensitive
def test_search_multiplecase():
    user0, _, _, expectedmessages0 = initialisation()

    searchdict = search(user0['token'], "let's")
    messages = searchdict['messages']
    for i, msg in enumerate(messages):
        assert msg['message_id'] == expectedmessages0[i]['message_id']
        assert msg['u_id'] == expectedmessages0[i]['u_id']
        assert msg['message'] == expectedmessages0[i]['message']

# check for returning multiple strings over different channels
def test_search_multiplediffchannel():
    user0, _, _, expectedmessages1 = initialisation()

    searchdict = search(user0['token'], "e")
    messages = searchdict['messages']
    for i, msg in enumerate(messages):
        assert msg['message_id'] == expectedmessages1[i]['message_id']
        assert msg['channel_id'] == expectedmessages1[i]['channel_id']
        assert msg['u_id'] == expectedmessages1[i]['u_id']
        assert msg['message'] == expectedmessages1[i]['message']

# return empty for string that doesn't exist
def test_search_multiplestring():
    user0, _, _, _ = initialisation()

    assert search(user0['token'], "ahahhaaha") == {'messages': []}
# return empty for channel caller is not apart of
def test_search_notaprtofchannel():
    _, user1, _, _ = initialisation()

    assert search(user1['token'], "e") == {'messages': []}
# check for invalid token
def test_search_invalidtoken():
    user0, _, _, _ = initialisation()

    with pytest.raises(error.AccessError):
        search('hello', "hello")

