'''
Provide a list of all channels (and their associated details)
NOTE: assumption that it returns all public/private channels regardless of user permissions
'''
from channels import channels_listall, channels_create
from auth import auth_register, auth_login
from other import clear 
from test_helpers import create_one_test_user, create_two_test_users

# tests for listing one public channels
def test_channels_listall_public():

    clear()
    test_user0 = create_one_test_user()
    
    # test_user0 creates 1 public channel
    pub_channel0 = channels_create(test_user0['token'], "Public  Channel 0", True)
    pub_channel0_id = pub_channel0['channel_id']

    assert(channels_listall(test_user0['token']) == [
                                                    {
                                                        "channel_id": pub_channel0_id,
                                                        "name": pub_channel0['name']
                                                    },
                                                ])

# tests for listing one private channels
def test_channels_listsall_private():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 private channel
    priv_channel0 = channels_create(test_user0['token'], "Private Channel 0", False)
    priv_channel0_id = priv_channel0['channel_id']

    assert(channels_listall(test_user0['token']) == [
                                                {
                                                    "channel_id": priv_channel0_id,
                                                    "name": priv_channel0['name']
                                                },
                                            ])

# tests for listing one of each public and private channels
def test_channels_listsall_both():

    clear()
    test_user0 = create_one_test_user()

    # test_user0 creates 1 public channel
    pub_channel0 = channels_create(test_user0['token'], "Public  Channel 0", True)
    pub_channel0_id = pub_channel0['channel_id']

    # test_user0 creates 1 private channel
    priv_channel0 = channels_create(test_user0['token'], "Private Channel 0", False)
    priv_channel0_id = priv_channel0['channel_id']

    assert(channels_listall(test_user0['token']) == [
                                            {
                                                "channel_id": pub_channel0_id,
                                                "name": pub_channel0['name']
                                            },
                                            {
                                                "channel_id": priv_channel0_id,
                                                "name": priv_channel0['name']
                                            },
                                        ])

# tests for listing many of each public and private channels
def test_channels_listsall_many():
        
    clear()
    test_user0, test_user1 = create_two_test_users()
    
    # create multiple test channels

    # test_user0 creates 1 public channel
    pub_channel0 = channels_create(test_user0['token'], "Public  Channel 0", True)
    pub_channel0_id = pub_channel0['channel_id']

    # test_user0 creates 1 private channel
    priv_channel0 = channels_create(test_user0['token'], "Private Channel 0", False)
    priv_channel0_id = priv_channel0['channel_id']

    # test_user1 creates 1 public channel
    pub_channel1 = channels_create(test_user1['token'], "Public  Channel 1", True)
    pub_channel1_id = pub_channel1['channel_id']

    # test_user1 creates 1 private channel
    priv_channel1 = channels_create(test_user1['token'], "Private Channel 1", False)
    priv_channel1_id = priv_channel1['channel_id']

    assert(channels_listall(test_user0_token) == [
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
