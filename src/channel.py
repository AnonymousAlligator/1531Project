from other import data
import error

def channel_invite(token, channel_id, u_id):
    return {
    }

def channel_details(token, channel_id):
    # Check that the token is valid
    for user in data['users']:
        # Token is valid
        if token == user['token']:
            # Find the channel
            for channel in data['channels']:
                # If we find the channel..
                if channel_id == channel['id']:
                    # Check to see if the user is part of that channel
                    for member in channel['all_members']:
                        if member['u_id'] == user['u_id']:
                            # Store the name of the channel
                            channel_name = channel['name']
                            # Look for each owner's details in the user data field by referenceing the u_id
                            channel_owners = []
                            for owner in channel['owner_members']:
                                for owner_details in data['users']:
                                    if owner['u_id'] == owner_details['u_id']:
                                        channel_owners.append({'u_id': owner_details['u_id'],
                                                                'name_first': owner_details['name_first'],
                                                                'name_last': owner_details['name_last'],
                                },)
                            # Look for each members details in the user data field by referenceing the u_id
                            channel_members = []
                            for member in channel['all_members']:
                                for member_details in data['users']:
                                    if member['u_id'] == member_details['u_id']:
                                        channel_members.append({'u_id': member_details['u_id'],
                                                                'name_first': member_details['name_first'],
                                                                'name_last': member_details['name_last'],
                                },)
                            return {'name': channel_name,
                                    'owner_members': channel_owners,
                                    'all_members': channel_members,
                                    }
                    # If we are here then the user isnt in the channel
                    raise error.AccessError('You are not part of the channel you want details about')
            # If we are here then that means the channel id couldnt be found
            raise error.InputError('The channel you have entered does not exist')
    # If we are here then the token was invalid
    raise error.AccessError('Invalid token recieved')

def channel_messages(token, channel_id, start):
    # Check that the token is valid
    for user in data['users']:
        # Token is valid
        if token == user['token']:
            # Find the channel
            for channel in data['channels']:
                # If we find the channel..
                if channel_id == channel['id']:
                     # Check to see if the user is part of that channel
                    for member in channel['all_members']:
                        if member['u_id'] == user['u_id']:
                            # Looping through the message data of the channel
                            message_data = []
                            number_of_messages = len(channel['messages'])
                            message_number = start
                            end = 0
                            # Check if start is beyond range of messages
                            if start >= number_of_messages:
                                raise error.InputError('The start value entered is older than all messages')
                            # Check to see if start is the least recent message
                            elif start == (number_of_messages - 1):
                                message = channel['messages'][start]
                                message_data.append(message)
                                return {'messages': message_data, 
                                        'start': start, 
                                        'end': -1,}
                            # We can iterate from start until either end or start + 50
                            else:
                                while (message_number < number_of_messages) and (end <= start + 49):
                                    message = channel['messages'][message_number]
                                    message_data.append(message)
                                    message_number += 1
                                    end += 1
                                return {'messages': message_data,
                                        'start': start,
                                        'end': end,}
                    # If we are here then the user isnt in the channel
                    raise error.AccessError('You are not part of the channel you want details about')
            # If we are here then that means the channel id couldnt be found
            raise error.InputError('The channel you have entered does not exist')
    # If we are here then the token was invalid
    raise error.AccessError('Invalid token recieved')

def channel_leave(token, channel_id):
    # Check that the token is valid
    for user in data['users']:
        # Token is valid
        if token == user['token']:
            # Check for if the channel_id is valid
            for channel in data['channels']:
                # If we find the channel..
                if channel_id == channel['id']:
                    # ..we now check if the user is a member of the channel
                    for member in channel['all_members']:
                        if token == member['token']:
                            # If they are a member of the channel, remove them
                            channel['all_members'].remove(member)
                            channel['owner_members'].remove(member)
                                # If there is now no one in the channel, delete the channel
                            if len(channel['all_members']) == 0:
                                data['channels'].remove(channel)
                            return {}
                    # If we are here then the person is not a member of the channel
                    raise error.AccessError('You are not a member of the channel you are trying to leave')
            # If we're here then we didn't find the channel so input error
            raise error.InputError('The channel you are trying to leave does not exist')
    # If we are here then the token was invalid
    raise error.AccessError('Invalid token recieved')

def channel_join(token, channel_id):
    # Check that the token is valid
    for user in data['users']:
        # Token is valid
        if token == user['token']:
            # Check for if the channel_id is valid
            for channel in data['channels']:
                # If we find the channel..
                if channel_id == channel['id']:
                    # ..we now check if the user is the flockr owner (u_id == 0)
                    # If they are the flockr owner then add them to the channel and make them an owner
                    if user['u_id'] == 0:
                        channel['all_members'].append({'u_id': user['u_id'], 'token': user['token']},)
                        channel['owner_members'].append({'u_id': user['u_id'], 'token': user['token']},)
                        return {}
                    # Otherwise, check to see if the channel they are joining is private
                    elif channel['is_public'] == False:
                        raise error.AccessError('The channel you are trying to join is private')
                    else:
                        # Channel is public so we add their details into the channel list
                        channel['all_members'].append({'u_id': user['u_id'], 
                                                        'token': user['token'],
                                                        },)
                        return {}
            # If we're here then we didn't find the channel so input error
            raise error.InputError('The channel you are trying to join does not exist')
    # If we are here then the token was invalid
    raise error.AccessError('Invalid token recieved')

def channel_addowner(token, channel_id, u_id):
    #check if channel exists
    for channels in data['channels']:
        if channel_id == channels['id']:
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
            elif token in channel['owner_members']:
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
                                #if there are no more owners remaining, loops through all memebers and sees if the removed owner 
                                #finds next person in all memebers and makes them owner
                     return{}
                else:
                    raise  error.InputError('The member you are trying to remove is not an owner of the channel')
            else:
                raise error.AccessError('You are not an owner of the channel and cannot remove owners')
        else:
            raise error.InputError('The channel you are trying to access does not exists')
    return {
    }    
