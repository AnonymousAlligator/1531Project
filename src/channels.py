from other import data, check_token
import error

def channels_list(token):
        
    user = check_token(token)   
    
    for user in data['users']:
        if token == user['token']:
            u_id = user['u_id']

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

#Provide a list of all channels (and their associated details)
def channels_listall(token):

    # check for valid user
    check_token(token)

    channels_listalls = {}        
    channel_list = []
    channel_info = {}    

    for channel in data['channels']:
        # if channel['is_public'] is True or user['u_id'] in channel['all_members']:
        # current assumption is that listall lists all public & private channels
        channel_info = {'channel_id': channel['id'],
                        'name': channel['name']}
        channel_list.append(channel_info)
    channels_listalls['channels'] = channel_list
    return channels_listalls

def channels_create(token, name, is_public):
    if len(name) > 20:
        raise error.InputError('Channel name is more than 20 characters')
    else:
        # Find user details in the user field of data
        for user in data['users']:
            # Found the user, now making the channel
            if token == user['token']:
                # Channel id is equivalent to last channel's id plus 1 or 0 if empty
                if len(data['channels']) == 0:
                    channel_id = 0
                else:
                    channel_id = data['channels'][-1]['id'] + 1
                data['channels'].append({'id': channel_id,
                                         'name': name,
                                         'is_public': is_public,
                                         'owner_members': [{'u_id': user['u_id'],'name_first': user['name_first'],'name_last': user['name_last'], 'profile_img_url': user['profile_img_url']}],
                                         'all_members': [{'u_id': user['u_id'],'name_first': user['name_first'],'name_last': user['name_last'], 'profile_img_url': user['profile_img_url']}],
                                         'messages': [],
                                        })
                return {'channel_id': channel_id}
        raise error.AccessError('Invalid token recieved')