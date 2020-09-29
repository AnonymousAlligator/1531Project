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
                        channels['all_members'].append({
                                                        'u_id': users['u_id'], 
                                                        'token': users['token'],
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
            #checks that they are not already an owner
            for member in channels['owner_members']
                if u_id == owner_members['u_id']
                    raise error.AccessError('You are already an owner of this channel.')
                    return {}
            for member in channels['all members']
                if u_id == all_members['u_id']
                    channels['owner_members'].append({'u_id' : })


            #checks that the user is a member of the channel
            elif u_id == all_members['u_id']
                channels['owner_members: [


                if token == user


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