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
    # Check for if the channel_id is valid
    for channel in data['channels']:
        # If we find the channel..
        if channel_id == channel['id']:
            # ..we now check if the user is a member of the channel
            for user in channel['all_members']:
                if token == user['token']:
                    # If they are a member of the channel, remove them
                    channel['all_members'].remove(user)
                    return {}
            # If we are here then the person is not a member of the channel
                raise error.AccessError('You are not a member of the channel you are trying to leave')
    # If we're here then we didn't find the channel so input error
    raise error.InputError('The channel you are trying to leave does not exist')
    return {
    }

def channel_join(token, channel_id):
    # Check for if the channel_id is valid
    for channel in data['channels']:
        # If we find the channel..
        if channel_id == channel['id']:
            # ..we now check if the user is the flockr owner (u_id == 0)
            for user in data['users']:
                if token == user['token']:
                    # If they are the flockr owner then add them to the channel and make them an owner
                    if user['u_id'] == 0:
                        channel['all_members'].append({'u_id': user['u_id'], 'token': user['token']})
                        channel_addowner(token, channel_id, user['u_id'])
                        return {}
                    # Otherwise, check to see if the channel they are joining is private
                    elif channel['is_public'] == False:
                        raise error.AccessError('The channel you are trying to join is private')
                    else:
                        # Channel is public so we add their details into the channel list
                        channel['all_members'].append({
                                                        'u_id': user['u_id'], 
                                                        'token': user['token'],
                                                        })
                        return {}
    # If we're here then we didn't find the channel so input error
    raise error.InputError('The channel you are trying to join does not exist')
    return {
    }

def channel_addowner(token, channel_id, u_id):
    #check if channel exists
    for channels in data['channels']:
        if channel_id == channels['id']:
            #checks that the caller is an owner
            for owner in channels['owner_members']:


                
                if token == owner_members['token']:
                   #then we check the user is member of the channel
                    for member in channels['all members']:
                        if u_id == all_members['token']:
                        channels['owner_members'].append({'u_id' : u_id, 'token': token}),
                        return {}
            raise error.AccessError('You are not an owner of the flockr and cannot add owners')


            
             raise error.InputError('You are already an owner of this channel.')
                    return {}
            #checks that the user is a member of the channel



            if channels['is_public'] == False:
                #check if user is member
                #raise error.AccessError('The authorised user is not in the channel')
        else:
            raise error.InputError('The channel you are trying to join does not exists')
    return {
    }    
    
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }