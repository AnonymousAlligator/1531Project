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
                                                        },)
                        return {}
    # If we're here then we didn't find the channel so input error
    raise error.InputError('The channel you are trying to join does not exist')

def channel_addowner(token, channel_id, u_id):
    #check if channel exists
    for channels in data['channels']:
        if channel_id == channels['id']:
            #If a new channel with no owners, make token owner.
            if len(channels['owner_members']) == 0:
                 channels['owner_members'].append({'u_id' : u_id, 'token': token}),
                 return {}
            #Checks that the caller is an owner
            for owner in channels['owner_members']:
                #If the caller is trying to add themselves as owner we raise error
                if token == owner['token'] and u_id == owner['token']:
                    raise error.InputError('You are already an owner of this channel.')
                #If caller is an owner, we will give permision
                elif token == owner['token']:
                   #then we check the user is member of the channel
                    for member in channels['all members']:
                        if u_id == member['u_id']:
                            for users in data['users']:
                                if u_id == users['u_id']:
                                    channels['owner_members'].append({'u_id' : u_id, 'token': users[token]}),
                                    return {}
                    raise error.InputError('The member you are trying to add is not part of the channel')
                raise error.AccessError('You are not an owner of the flockr and cannot add owners')
        else:
            raise error.InputError('The channel you are trying to join does not exists')
    return {
    }    



def channel_removeowner(token, channel_id, u_id):
    #Check if channel exists
    for channel in data['channels']:
        if channel_id == channel['id']:
            if len(channels['all_members']) == 1:
            #TD: weird edge case
            #Checks to see if the member is an owner of the channel
            else token in channel['owner_members']:
                #Checks if the person is removing themselves as an owner. 
                if token == u_id:
                #if they are the last person in the owner list,     
                    if len(channels['owner_members']) == 1:
                        #TD: Call removeowner helper. 
                        #TD: check where they are on the members list, if they are at the front then choose
                            #next person to be owner, otherwise go to the front of owner_members and choose person. 
                        #TD: Call addowner to the first person in all members
                    else:
                        #TD: Call removeowner helper.
                        return {}
                else: 
                    #TD: Call removeowner helper.

                    if u_id in channel['owner_members']:
                        for owner in channels['owner_members']:
                            if u_id == owner['uid']:
                                channels['owner_members'].remove(owner)
                                #if there are no more owners remaining, loops trhough all memebers and sees if the removed owner 
                                #finds next person in all memebers and makes them 
                                return{}
                else:
                    raise  error.InputError('The member you are trying to remove is not an owner of the channel')
            else:
                raise error.AccessError('You are not an owner of the channel and cannot remove owners')
        else:
            raise error.InputError('The channel you are trying to access does not exists')
    return {
    }    
