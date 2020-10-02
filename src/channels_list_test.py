'''
Provide a list of all channels (and their associated details) that the authorised user is part of
'''
from channels import channels_list, channels_create
from channel import channel_join, channel_invite
from auth import auth_register, auth_login
from other import clear
from test_helpers import create_one_test_user, create_two_test_users

# user0 creates 1 channel. check that listall returns that one channel
# user0 then creates another. check that listall now lists 2 channels
def test_channels_listsall_one_user_channel():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    pub_channel0 = channels_create(test_user0['token'], "Public Channel 0", True)
    pub_channel0_id = pub_channel0['channel_id']

    # check returns 1 authorised channel
    assert(channels_list(test_user0['token']) == [
                                    {
                                        "channel_id": pub_channel0_id,
                                        "name": pub_channel0['name']
                                    },
                                ])

    # test_user0 creates 1 private channel
    priv_channel0 = channels_create(test_user0['token'], "Private Channel 0", False)
    priv_channel0_id = priv_channel0['channel_id']

    # check returns 2 authorised channels
    assert(channels_list(test_user0['token']) == [
                                            {
                                                "channel_id": pub_channel0_id,
                                                "name": pub_channel0['name']
                                            },
                                            {
                                                "channel_id": priv_channel0_id,
                                                "name": priv_channel0['name']
                                            },
                                        ])


# user0 creates 1 public, 1 private channel. user1 joins only 1 public channel.
# check that for user1, only return the public channel they are part of
def test_channels_list_authorised_pub_channel():
    
    clear()
    test_user0, test_user1 = create_two_test_users()

    # test_user0 creates 1 public channel
    pub_channel0 = channels_create(test_user0['token'], "Public Channel 0", True)
    pub_channel0_id = pub_channel0['channel_id']

    # test_user0 creates 1 private channel
    channels_create(test_user0['token'], "Private Channel 0", False)

    # test_user1 joins public channel
    channel_join(test_user1['token'], pub_channel0_id)

    # for test_user1, only lists the 1 public channel they are part of
    assert(channels_list(test_user1['token']) == [
                                        {
                                            "channel_id": pub_channel0_id,
                                            "name": pub_channel0['name']
                                        },
                                    ])

# user0 creates 1 public, 1 private channel. user1 joins only 1 private channel.
# check that for user1, only return the private channel they are part of
def test_channels_list_authorised_priv_channel():
    
    clear()
    test_user0, test_user1 = create_two_test_users()

    # test_user0 creates 1 public channel
    channels_create(test_user0['token'], "Public  Channel 0", True)

    # test_user0 creates 1 private channel
    priv_channel0 = channels_create(test_user0['token'], "Private Channel 0", False)
    priv_channel0_id = priv_channel0['channel_id']

    # test_user1 is invited to join private channel
    channel_invite(test_user1['token'], priv_channel0_id, test_user1['u_id'])

    # for test_user1, only lists the 1 private channel they are part of
    assert(channels_list(test_user1['token']) == [
                                        {
                                            "channel_id": priv_channel0_id,
                                            "name": priv_channel0['name']
                                        },
                                    ])

# user0 and user1 both create one of each public and private channels. user1 joins all 4 channels.
# check that for user0, return only the 2 channels they created
def test_channels_listsall_owner_channels():

    clear()
    test_user0, test_user1 = create_two_test_users()

    # test_user0 creates 1 public channel
    pub_channel0 = channels_create(test_user0['token'], "Public Channel 0", True)
    pub_channel0_id = pub_channel0['channel_id']

    # test_user0 creates 1 private channel
    priv_channel0 = channels_create(test_user0['token'], "Private Channel 0", False)
    priv_channel0_id = priv_channel0['channel_id']

    # test_user1 creates 1 public channel
    channels_create(test_user1['token'], "Public  Channel 1", True)

    # test_user1 creates 1 private channel
    channels_create(test_user1['token'], "Private Channel 1", False)

    # check that for user0, return only the 2 channels they created
    assert(channels_list(test_user1['token']) == [
                                                {
                                                    "channel_id": pub_channel0_id,
                                                    "name": pub_channel0['name']
                                                },
                                                {
                                                    "channel_id": priv_channel0_id,
                                                    "name": priv_channel0['name']
                                                },
                                            ])


# user0 and user1 both create one of each public and private channels. user1 joins all 4 channels.
# check that for user1, return list of all channels
def test_channels_listsall_joined_channels():

    clear()
    test_user0, test_user1 = create_two_test_users()

    # test_user0 creates 1 public channel
    pub_channel0 = channels_create(test_user0['token'], "Public Channel 0", True)
    pub_channel0_id = pub_channel0['channel_id']

    # test_user0 creates 1 private channel
    priv_channel0 = channels_create(test_user0['token'], "Private Channel 0", False)
    priv_channel0_id = priv_channel0['channel_id']

    # test_user1 creates 1 public channel
    pub_channel1 = channels_create(test_user1['token'], "Public Channel 1", True)
    pub_channel1_id = pub_channel1['channel_id']

    # test_user1 creates 1 private channel
    priv_channel1 = channels_create(test_user1['token'], "Private Channel 1", False)
    priv_channel1_id = priv_channel1['channel_id']

    # test_user1 joins the channels test_user0 created
    channel_join(test_user1['token'], pub_channel0_id)
    channel_invite(test_user1['token'], priv_channel0_id, test_user1['u_id'])

    # check that for test_user1, return list of all channels
    assert(channels_list(test_user1['token']) == [
                                            {
                                                "channel_id": pub_channel0_id,
                                                "name": pub_channel0['name']
                                            },
                                            {
                                                "channel_id": priv_channel0_id,
                                                "name": priv_channel0['name']
                                            },
                                            {
                                                "channel_id": pub_channel1_id,
                                                "name": pub_channel1['name']
                                            },
                                            {
                                                "channel_id": priv_channel1_id,
                                                "name": priv_channel1['name']
                                            },
                                        ])



