from channels import channels_listall

#Provide a list of all channels (and their associated details) that the authorised user is part of

def test_channels_list_exists():
    assert channels_list(token) == print({channels})

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