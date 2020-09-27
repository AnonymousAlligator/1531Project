from channels import channels_list
import error


def test_channels_list_exists():
    assert channels_list('token') == {channels}

"""
def channels_list(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }
"""