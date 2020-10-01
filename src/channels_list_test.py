'''
Provide a list of all channels (and their associated details) that the authorised user is part of
'''
from channels import channels_list, channels_create
from channel import channel_join, channel_invite
from auth import auth_register, auth_login
# from other import clear #TODO: uncomment once merged into all_tests

# register test users
test_user0 = auth_register("test_0@email.com", "0password0", "Hayden", "Jacobs") #returns { u_id, token }
test_user1 = auth_register("test_1@email.com", "1password1", "Jayden", "Haycobs") #returns { u_id, token }

# get registered users tokens
test_user0_token = test_user0['token']
test_user1_token = test_user1['token']

# get registered users u_ids
test_user1_id = test_user1['u_id']

# user0 creates 1 public, 1 private channel. user1 joins only 1 public channel.
# check that for user1, only return the public channel they are part of
def test_channels_list_authorised_pub_channel():
    # clear()

    # test_user0 creates 1 public channel
    pub_channel0 = channels_create(test_user0_token, "Public Channel 0", True)
    pub_channel0_id = pub_channel0['channel_id']

    # test_user0 creates 1 private channel
    channels_create(test_user0_token, "Private Channel 0", False)

    # test_user1 joins public channel
    channel_join(test_user1_token, pub_channel0_id)

    # for test_user1, only lists the 1 public channel they are part of
    assert(channels_list(test_user1_token) == [
                                        {
                                            "channel_id": pub_channel0_id,
                                            "name": pub_channel0['name']
                                        },
                                    ])

# user0 creates 1 public, 1 private channel. user1 joins only 1 private channel.
# check that for user1, only return the private channel they are part of
def test_channels_list_authorised_priv_channel():
    # clear()

    # test_user0 creates 1 public channel
    channels_create(test_user0_token, "Public  Channel 0", True)

    # test_user0 creates 1 private channel
    priv_channel0 = channels_create(test_user0_token, "Private Channel 0", False)
    priv_channel0_id = priv_channel0['channel_id']

    # test_user1 is invited to join private channel
    channel_invite(test_user1_token, priv_channel0_id, test_user1_id)

    # for test_user1, only lists the 1 private channel they are part of
    assert(channels_list(test_user1_token) == [
                                        {
                                            "channel_id": priv_channel0_id,
                                            "name": priv_channel0['name']
                                        },
                                    ])

# user0 and user1 both create one of each public and private channels. user1 joins all 4 channels.
# check that for user0, return only the 2 channels they created
def test_channels_listsall_owner_channels():
    # clear()

    # test_user0 creates 1 public channel
    pub_channel0 = channels_create(test_user0_token, "Public Channel 0", True)
    pub_channel0_id = pub_channel0['channel_id']

    # test_user0 creates 1 private channel
    priv_channel0 = channels_create(test_user0_token, "Private Channel 0", False)
    priv_channel0_id = priv_channel0['channel_id']

    # test_user1 creates 1 public channel
    channels_create(test_user1_token, "Public  Channel 1", True)

    # test_user1 creates 1 private channel
    channels_create(test_user1_token, "Private Channel 1", False)

    # check that for user0, return only the 2 channels they created
    assert(channels_list(test_user0_token) == [
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
    # clear()

    # test_user0 creates 1 public channel
    pub_channel0 = channels_create(test_user0_token, "Public Channel 0", True)
    pub_channel0_id = pub_channel0['channel_id']

    # test_user0 creates 1 private channel
    priv_channel0 = channels_create(test_user0_token, "Private Channel 0", False)
    priv_channel0_id = priv_channel0['channel_id']

    # test_user1 creates 1 public channel
    pub_channel1 = channels_create(test_user1_token, "Public Channel 1", True)
    pub_channel1_id = pub_channel1['channel_id']

    # test_user1 creates 1 private channel
    priv_channel1 = channels_create(test_user1_token, "Private Channel 1", False)
    priv_channel1_id = priv_channel1['channel_id']

    # test_user1 joins the channels test_user0 created
    channel_join(test_user1_token, pub_channel0_id)
    channel_invite(test_user1_token, priv_channel0_id, test_user1_id)

    # check that for test_user1, return list of all channels
    assert(channels_list(test_user1_token) == [
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



