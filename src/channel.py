from other import data
import error

def channel_invite(token, channel_id, u_id):
    return {
    }

def channel_details(token, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages(token, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave(token, channel_id):
    return {
    }

def channel_join(token, channel_id):
    # Check for if the channel_id is valid
    for channels in data['channels']:
        # If we find the channel..
        if channel_id == channels['id']:
            # ..we now check if the user is the flockr owner (u_id == 0)
            for users in data['users']:
                if token == users['token']:
                    # If they are the flockr owner then add them to the channel and make them an owner
                    if users['u_id'] == 0:
                        channels['all_members'].append({'u_id': users['u_id'], 'token': users['token']})
                        channel_addowner(token, channel_id, users['u_id'])
                        return {}
                    # Otherwise, check to see if the channel they are joining is private
                    elif channels['is_public'] == False:
                        raise error.AccessError('The channel you are trying to join is private')
                    else:
                        # Channel is public so we add their details into the channel list
                        channels['all_members'].append({'u_id': users['u_id'], 'token': users['token']})
                        return {}
    # If we're here then we didn't find the channel so input error
    raise error.InputError('The channel you are trying to join does not exist')

def channel_addowner(token, channel_id, u_id):
    #Checks if channel exists
    for channels in data['channels']:
        if channel_id == channels['id']:
            #checks that the caller is an owner
            if len(channels['owner_members']) == 0:
                 channels['owner_members'].append({'u_id' : u_id, 'token': token}),
                 return {}
            for owner in channels['owner_members']:
                #If the caller is trying to add themselves as owner we raise error
                if token == owner['token'] and u_id == owner['token']:
                    raise error.InputError('You are already an owner of this channel.')
                #If the 
                elif token == owner['token']:
                   #then we check the user is member of the channel
                    for member in channels['all members']:
                        if u_id == member['u_id']:
                            for users in data['users']:
                                if u_id == users['u_id']:
                                    channels['owner_members'].append({'u_id' : u_id, 'token': users[token]}),
                                    return {}
                    raise error.InputError('The member you are trying to add is not part of the channel')
                    return {}
            raise error.AccessError('You are not an owner of the flockr and cannot add owners')
            return {}
        else:
            raise error.InputError('The channel you are trying to join does not exists')
    return {}    


def channel_removeowner(token, channel_id, u_id):
    return {
    }