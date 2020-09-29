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
    if len(string) > 20:
        raise error.InputError('Channel name is more than 20 characters')
    else:
        for channels in data['channels']:
            if token == users['token']:
                for users in data['users']:
                    if token == users['token']:
                        channel_id = len(backend_data['channels'])
                        data['channels'].append({'channel_id': channel_id, 'name': name, 'is_public': is_public, 'owner_members':{users[u_id], user[token]} 'all_members': {users[u_id], user[token]}})
                        return {channel_id}
    return {
    }
