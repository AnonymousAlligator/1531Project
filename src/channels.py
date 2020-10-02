from other import data
import error

def channels_list(token):
        
    #TODO: add in taimoor's user check
    # check for valid user
    for u in data['users']:
        for valid_token in user['tokens']:
            if valid_token == token:
                user = u
    
    # list of channels the authorised user is part of
    channels_list = []                

    # get all channels info
    for channel in data['channels']: 
        for member_id in channel['all_members']:
            if member_id == user['u_id']:
                channel_info = {
                                'channel_id': channel['id'],
                                'name': channel['name']
                                }
                channels_list.append(channel_info)

    return channels_list

'''Provide a list of all channels (and their associated details)'''
def channels_listall(token):

    #TODO: add in taimoor's user check
    # check for valid user
    for u in data['users']:
        for valid_token in user['tokens']:
            if valid_token == token:
                user = u

    
    channels_listall = []

    for channel in data['channels']:
        # if channel['is_public'] is True or user['u_id'] in channel['all_members']:
        # current assumption is that listall lists all public & private channels
        if user['u_id'] in channel['all_members']:
            channel_info = {'channel_id': channel['id'],
                            'name': channel['name']}
            channels_listall.append(channel_info)

    return channels_listall

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
                data['channels'].append({'id': channel_id,
                                         'name': name,
                                         'is_public': is_public,
                                         'owner_members': [{user['u_id']}],
                                         'all_members': [{user['u_id']}],
                                         'messages': [],
                                        })
                return channel_id
