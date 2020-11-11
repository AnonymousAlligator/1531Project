from other import data, check_token
import error

def channels_list(token):
    # Check that the token is valid
    caller = check_token(token)
    u_id = caller['u_id']
    channels = {}
    channel_list = []
    channel_info = {}
    # get all channels info
    for channel in data['channels']:
        for member_id in channel['all_members']:
            if member_id['u_id'] == u_id:
                channel_info = {
                                'channel_id': channel['id'],
                                'name': channel['name']
                                }
                channel_list.append(channel_info)
    channels['channels'] = channel_list
    return channels

def channels_listall(token):
    # check that the token is valid
    check_token(token)

    channels_listalls = {}        
    channel_list = []
    channel_info = {}    

    for channel in data['channels']:
        channel_info = {'channel_id': channel['id'],
                        'name': channel['name']}
        channel_list.append(channel_info)
    channels_listalls['channels'] = channel_list
    return channels_listalls

def channels_create(token, name, is_public):
    # Check the token is valid
    caller = check_token(token)

    # Check channel name length
    if len(name) > 20:
        raise error.InputError('Channel name is more than 20 characters')

    # Assigning channel ID, empty = 0 else last ID+1
    if len(data['channels']) == 0:
        channel_id = 0
    else:
        channel_id = data['channels'][-1]['id'] + 1
    data['channels'].append({'id': channel_id,
                                'name': name,
                                'is_public': is_public,
                                'owner_members': [{'u_id': caller['u_id'],
                                                    'name_first': caller['name_first'],
                                                    'name_last': caller['name_last'], 
                                                    'profile_img_url': caller['profile_img_url']}],
                                'all_members': [{'u_id': caller['u_id'],
                                                    'name_first': caller['name_first'],
                                                    'name_last': caller['name_last'], 
                                                    'profile_img_url': caller['profile_img_url']}],
                                'messages': [],
                                'standup': {'is_standup': False, 'time_finish': None},
                            })
    return {'channel_id': channel_id}
