'''
InputError when message does not exist
AccessError when message_id was not sent by the user or when the user is not owner of the channel
'''

from channel import channel_invite, channel_addowner, channel_join
from channels import channels_create
from message import message_send, message_remove
from test_helpers import create_one_test_user, create_two_test_users, create_three_test_users
from error import AccessError, InputError
from other import clear
import pytest

# check func works when 1 user (owner) in public channel, sends 1 message and removes it
def test_message_remove_works_public():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    public_channel_id = channels_create(test_user0['token'], "Public Channel", True)

    # test_user0 sends 1 message to public channel
    message0 = "Let's geddit"
    message0_id = message_send(test_user0['token'], public_channel_id, message0)

    # assert func works for public channel
    assert message_remove(test_user0['token'], message0_id['message_id']) == {}

# check func works when 1 user (owner) in private channel, sends 1 message and removes it
def test_message_remove_works_private():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 private channel
    private_channel_id = channels_create(test_user0['token'], "Private Channel", False)

    # test_user0 sends 1 message to public channel
    message0 = "Let's geddit"
    message0_id = message_send(test_user0['token'], private_channel_id, message0)

    # assert func works for private channel
    assert message_remove(test_user0['token'], message0_id['message_id']) == {}

# check func works when 2 users in channel, user1 (not owner) sends message and removes it
def test_message_remove_works_more_people_channel():

    clear()
    test_user0, test_user1 = create_two_test_users()

    # test_user0 creates 1 public channel
    public_channel_id = channels_create(test_user0['token'], "Main Channel", True)

    # test_user1 joins public channel
    channel_join(test_user1['token'], public_channel_id)

    # test_user1 sends 1 message
    message0 = "Let's geddit"
    message0_id = message_send(test_user1['token'], public_channel_id, message0)

    # check test_user1 (member) removes their message
    assert message_remove(test_user1['token'], message0_id['message_id']) == {}

# check channel owner can remove messages
def test_message_remove_works_more_people_channel():

    clear()
    test_user0, test_user1 = create_two_test_users()

    # test_user0 creates 1 public channel
    public_channel_id = channels_create(test_user0['token'], "Main Channel", True)

    # test_user1 joins public channel
    channel_join(test_user1['token'], public_channel_id)

    # test_user1 sends 1 message
    message0 = "Let's geddit"
    message0_id = message_send(test_user1['token'], public_channel_id, message0)

    # check test_user1 (channel owner) removes their message
    assert message_remove(test_user0['token'], message0_id['message_id']) == {}

# check flockr owner can remove messages
def test_message_remove_works_more_people_channel():

    clear()
    test_user0, test_user1, test_user2 = create_three_test_users()

    # test_user1 creates 1 public channel
    public_channel_id = channels_create(test_user1['token'], "Main Channel", True)

    # test_user2 joins public channel
    channel_join(test_user2['token'], public_channel_id)

    # test_user1 sends 1 message
    message0 = "Let's geddit"
    message0_id = message_send(test_user1['token'], public_channel_id, message0)

    # check test_user0 (flockr owner) removes their message
    assert message_remove(test_user0['token'], message0_id['message_id']) == {}

# check user can't remove an already deleted message
def test_message_remove_already_deleted_msg():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 private channel
    private_channel_id = channels_create(test_user0['token'], "Private Channel", False)

    # test_user0 sends 1 message to public channel
    message0 = "Let's geddit"
    message0_id = message_send(test_user0['token'], private_channel_id, message0)

    # test_user0 removes message
    assert message_remove(test_user0['token'], message0_id['message_id']) == {}

    # test_user0 tries to call remove for a deleted message
    with pytest.raises(InputError):
        assert message_remove(test_user0['token'], message0_id['message_id'])

# check user0 can't remove user1's message
def test_message_remove_no_permission():
    clear()
    test_user0, test_user1 = create_two_test_users()

    # test_user0 creates 1 public channel
    public_channel_id = channels_create(test_user0['token'], "Main Channel", True)

    # test_user1 joins public channel
    channel_join(test_user1['token'], public_channel_id)

    # test_user0 sends 1 message
    message0 = "Let's geddit"
    message0_id = message_send(test_user0['token'], public_channel_id, message0)

    # test_user1 tries to remove test_user0's message
    with pytest.raises(AccessError):
        assert message_remove(test_user1['token'], message0_id['message_id'])
