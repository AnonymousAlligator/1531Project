from data import data
import error

'''Provide a list of all channels (and their associated details) that the authorised user is part of'''
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
                                'channel_id': channel['channel_id'],
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

    # assumption is that listall lists all public & private channels
    for channel in data['channels']:
        if channel['is_public'] is True or user['u_id'] in channel['all_members']:
            channel_info = {'channel_id': channel['channel_id'],
                            'name': channel['name']}
            channels_listall.append(channel_info)

    return channels_listall

def channels_create(token, name, is_public):
    return {
        'channel_id': 1,
    }
