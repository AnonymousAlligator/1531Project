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

@pytest.mark.skip(reason='function implementation not done yet')
# check func works when 1 user (owner) in public channel, sends 1 message and removes it
def test_message_remove_works_public():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    public_channel_id = channels_create(test_user0['token'], "Public Channel", True)

    # test_user0 sends 1 message to public channel
    message0_id = "Let's geddit"
    message_send(test_user0['token'], public_channel_id, message0_id)

    # assert func works for public channel
    assert message_remove(test_user0['token'], 1) == {} # TODO: update in iteration2

@pytest.mark.skip(reason='function implementation not done yet')
# check func works when 1 user (owner) in private channel, sends 1 message and removes it
def test_message_remove_works_private():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 private channel
    private_channel_id = channels_create(test_user0['token'], "Private Channel", False)

    # test_user0 sends 1 message to public channel
    message0_id = "Let's geddit"
    message_send(test_user0['token'], private_channel_id, message0_id)

    # assert func works for private channel
    assert message_remove(test_user0['token'], 1) == {} # TODO: update in iteration2

@pytest.mark.skip(reason='function implementation not done yet')
# check func works when 2 users in channel, user1 (not owner) sends message and removes it
def test_message_remove_works_more_people_channel():

    clear()
    test_user0, test_user1 = create_two_test_users()

    # test_user0 creates 1 public channel
    public_channel_id = channels_create(test_user0['token'], "Main Channel", True)

    # test_user1 joins public channel
    channel_join(test_user1['token'], public_channel_id)

    # test_user1 sends 1 message
    message0_id = "Let's geddit"
    message_send(test_user1['token'], public_channel_id, message0_id)

    # check test_user1 (member) removes their message
    assert message_remove(test_user1['token'], 1) == {} # TODO: update in iteration2

@pytest.mark.skip(reason='function implementation not done yet')
# check user can't remove an already deleted message
def test_message_remove_already_deleted_msg():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 private channel
    private_channel_id = channels_create(test_user0['token'], "Private Channel", False)

    # test_user0 sends 1 message to public channel
    message0_id = "Let's geddit"
    message_send(test_user0['token'], private_channel_id, message0_id)

    # test_user0 removes message
    message_remove(test_user0['token'], 1) == {} # TODO: update in iteration2

    # test_user0 tries to call remove for a deleted message
    with pytest.raises(InputError):
        message_remove(test_user0['token'], message0_id) == {}


@pytest.mark.skip(reason='function implementation not done yet')
# check user0 can't remove user1's message
def test_message_remove_user_remove_anothers():
    clear()
    test_user0, test_user1 = create_two_test_users()

    # test_user0 creates 1 public channel
    public_channel_id = channels_create(test_user0['token'], "Main Channel", True)

    # test_user1 joins public channel
    channel_join(test_user1['token'], public_channel_id)

    # test_user1 sends 1 message
    message0_id = "Let's geddit"
    message_send(test_user1['token'], public_channel_id, message0_id)

    # test_user0 tries to remove test_user1's message
    with pytest.raises(AccessError):
        message_remove(test_user0['token'], message0_id)
