'''
AccessError when message_id was not sent by the user or when the user is not owner of the channel
'''

from channel import channel_join
from channels import channels_create
from message import message_send, message_edit, message_remove
from test_helpers import create_one_test_user, create_two_test_users
from error import AccessError
from other import clear
import pytest
    
# check that editing a message works
def test_message_edit():
    
    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    channel_id = channels_create(test_user0['token'], "Public Channel", True)
        
    # test_user0 sends 1 message to public channel
    message0 = "inital message"
    message0_id = message_send(test_user0['token'], channel_id['channel_id'], message0)

    assert message_edit(test_user0['token'], message0_id['message_id'], 'edited message') == {}

# check that user1 cannot edit user0's message
def test_message_edit_notusermsg():

    clear()
    test_user0, test_user1 = create_two_test_users()

    # test_user0 creates 1 public channel
    public_channel_id = channels_create(test_user0['token'], "Main Channel", True)

    # test_user1 joins public channel 
    channel_join(test_user1['token'], public_channel_id['channel_id'])
        
    # test_user0 sends 1 message
    message0 = "user0's message"
    message0_id = message_send(test_user0['token'], public_channel_id['channel_id'], message0)
    
    # raise error if user1 tries to edit user0's message
    with pytest.raises(AccessError):
        message_edit(test_user1['token'], message0_id['message_id'], 'edited message')
    