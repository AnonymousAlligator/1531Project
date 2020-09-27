from channels import channels_listall

#Provide a list of all channels (and their associated details) that the authorised user is part of
user_0 = auth_register("apples@email.com", "applepass", "apple", "red") #returns { u_id, token }




def test_channels_list_exists():
    assert channels_list(user_0 'token') == {channels}

"""
def channels_listall(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }
"""