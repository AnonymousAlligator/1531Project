'''
InputError when message does not exist
AccessError when message_id was not sent by the user or when the user is not owner of the channel
'''

from channel import channel_invite, channel_addowner, channel_join
from channels import channels_create
from auth import auth_register
from message import message_send, message_remove
from test_helpers import create_one_test_user, create_two_test_users, create_three_test_users
from error import InputError
from other import clear
import pytest

# Jeffo = auth_register("Jeffo@email.com", "a1b2c3", "Jeffo", "Jeff")
# Smith = auth_register("smith@email.com", "a1b2c3", "Smith", "Smith")
# Tom = auth_register("tom@email.com", "a1b2c3", "Tom", "Tommery")

# check func works when 1 user (owner) in public channel, sends 1 message and removes it
def test_message_remove_works_public():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    public_channel_id = channels_create(test_user0['token'], "Public Channel", True)
        
    # test_user0 sends 1 message to public channel
    message0 = "Let's geddit"
    message_send(test_user0['token'], public_channel_id, message0)

    # assert func works for public channel    
    assert message_remove(test_user0['token'], 1) == {} # TODO: update in iteration2

# check func works when 1 user (owner) in private channel, sends 1 message and removes it
def test_message_remove_works_private():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 private channel
    private_channel_id = channels_create(test_user0['token'], "Private Channel", False)
        
    # test_user0 sends 1 message to public channel
    message0 = "Let's geddit"
    message_send(test_user0['token'], private_channel_id, message0)

    # assert func works for private channel    
    assert message_remove(test_user0['token'], 1) == {} # TODO: update in iteration2    

# check func works when 2 users in channel, user1 (not owner) sends message and removes it
def test_message_remove_works_more_people_channel():
    
    clear()
    test_user0, test_user1 = create_two_test_user()

    # test_user0 creates 1 public channel
    public_channel_id = channels_create(test_user0['token'], "Main Channel", True)

    # test_user1 joins public channel 
    channel_join(test_user1['token'], public_channel_id)
        
    # test_user1 sends 1 message
    message0 = "Let's geddit"
    message_send(test_user1['token'], 0, message0)

    # check test_user1 (member) removes their message
    assert message_remove(test_user1['token'], 1) == {} # TODO: update in iteration2    

# TODO
# def test_message_remove_messagenolonderexists():
#     with pytest.raises(error.InputError):
#         assert message_remove(Jeffo['token'], 3)

# def test_message_remove_messagedoesnotbelongtouser():
#     with pytest.raises(error.AccessError):
#         assert message_remove(Smith['token'], 0)

# def test_message_remove_isnotowner():
#     with pytest.raises(error.AccessError):
#         assert message_remove(Tom['token'], 0)