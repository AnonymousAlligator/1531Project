from other import data
import error

def channels_list(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create(token, name, is_public):
    if len(name) > 20:
        raise error.InputError('Channel name is more than 20 characters')
    else:
        # Find user details in the user field of data
        for user in data['users']:
            # Found the user, now making the channel
            if token == user['token']:
                # Channel id is equivalent to the size of channels field before making the channel
                channel_id = len(data['channels'])
                data['channels'].append({'channel_id': channel_id,
                                         'name': name,
                                         'is_public': is_public,
                                         'owner_members': [{user['u_id'], user['token']},],
                                         'all_members': [{user['u_id'], user['token']},],
                                         'messages': []
                                        })
                return {channel_id}
