'''
    Provide a list of all channels (and their associated details) that the authorised user is part of
'''
from data import data

def channels_list(token):
        
    # Check for valid user
    for u in data['users']:
        for valid_token in user['tokens']:
            if valid_token == token:
                user = u

    if user is None: 
        print'test' #TODO: update once channels tests are in
    
    # list of channels the authorised user is part of
    channels_list = []                

    # get all channels info
    for channel in data['channels']: 
        for member_id in channel['all_members']:
            if member_id == user['u_id']:
                channel_info = {
                                'channel_id': channel['channel_id'],
                                'name': channel['name']
                                }
                channels_list.append(channel_info)

    return channels_list

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
    return {
        'channel_id': 1,
    }
