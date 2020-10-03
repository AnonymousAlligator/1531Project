from other import data, check_token
from remove_owner_helper import *
import error

def channel_invite(token, channel_id, u_id):
    # Check that the token is valid
    inviter = check_token(token)

    # Check if user to be added exists within database
    invitee = {}
    for user in data['users']:
        if u_id == user['u_id']:
            invitee = user
    # Input Error if the user doesn't exist
    if invitee == {}:
        raise error.InputError('User you are trying to invite does not exist')

    # Find the channel
    target_channel = {}
    for channel in data['channels']:
        if channel_id == channel['id']:
            target_channel = channel
    # Input Error if the channel doesn't exist
    if target_channel == {}:
        #Input Error if the channel doesn't exist
        raise error.InputError('Channel does not exist')

    is_member = False
    # Check to see if inviter is part of that channel
    for member in target_channel['all_members']:
        if member['u_id'] == inviter['u_id']:
            is_member = True
    # Access Error if the person inviting is not within the server
    if is_member == False:
        raise error.AccessError('You can only invite people to channels you are apart of')  
    
    # Made it through all the checks so now we can add the invitee
    target_channel['all_members'].append({'u_id': invitee['u_id'], 
                                            'name_first': invitee['name_first'], 
                                            'name_last': invitee['name_last'],})
    # Also if u_id is 0, then make them an owner
    if u_id == 0:
        target_channel['owner_members'].append({'u_id': invitee['u_id'],
                                                'name_first': invitee['name_first'],
                                                'name_last': invitee['name_last'],})
    return {}

def channel_details(token, channel_id):
    # Check that the token is valid
    caller = check_token(token)
    
    # Find the channel
    target_channel = {}
    for channel in data['channels']:
        if channel_id == channel['id']:
            target_channel = channel
    # Input Error if the channel doesn't exist
    if target_channel == {}:
        #Input Error if the channel doesn't exist
        raise error.InputError('Channel does not exist')

    is_member = False
    # Check to see if inviter is part of that channel
    for member in target_channel['all_members']:
        if member['u_id'] == caller['u_id']:
            is_member = True
    # Access Error if the person inviting is not within the server
    if is_member == False:
        raise error.AccessError('You are not part of the channel you want details about') 

    # Made it through all checks so now we start building the return
    channel_name = channel['name']
    # Append owner details
    channel_owners = []
    for owner in channel['owner_members']:
        channel_owners.append({'u_id': owner['u_id'],
                                'name_first': owner['name_first'],
                                'name_last': owner['name_last'],})
    # Append member details
    channel_members = []
    for member in channel['all_members']:
        channel_members.append({'u_id': member['u_id'],
                                'name_first': member['name_first'],
                                'name_last': member['name_last'],})
    
    return {'name': channel_name,
            'owner_members': channel_owners,
            'all_members': channel_members,
            }


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
                        if user['u_id'] == member['u_id']:
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
                        channel['all_members'].append({'u_id': user['u_id'], 
                                                        'name_first': user['name_first'], 
                                                        'name_last': user['name_last']})
                        channel['owner_members'].append({'u_id': user['u_id'], 
                                                            'name_first': user['name_first'], 
                                                            'name_last': user['name_last']})
                        return {}
                    # Otherwise, check to see if the channel they are joining is private
                    elif channel['is_public'] == False:
                        raise error.AccessError('The channel you are trying to join is private')
                    else:
                        # Channel is public so we add their details into the channel list
                        channel['all_members'].append({'u_id': user['u_id'], 
                                                        'name_first': user['name_first'], 
                                                        'name_last': user['name_last']})
                        return {}
            # If we're here then we didn't find the channel so input error
            raise error.InputError('The channel you are trying to join does not exist')
    # If we are here then the token was invalid
    raise error.AccessError('Invalid token recieved')

def channel_addowner(token, channel_id, u_id):
    caller_data = find_with_token(token)
    for channel in data['channels']:
        if channel_id == channel['id']:
            #Checks that the caller is an owner
            for owner in channel['owner_members']:
                #If the caller is trying to add themselves as owner we raise error
                if caller_data[0] == owner['u_id'] and u_id == owner['u_id']:
                    raise error.InputError('You are already an owner of this channel.')
                #If caller is an owner, we will give permision
                elif caller_data[0] == owner['u_id']:
                   #If the user is not a member of the channel we raise error
                    for member in channel['all_members']:
                        #If user is a member, we append details to the owner_members
                        if u_id == member['u_id']:
                            for users in data['users']:
                                if u_id == users['u_id']:
                                    channel['owner_members'].append({'u_id' : caller_data[0], 'name_first': caller_data[1], 'name_last':caller_data[2],})
                                    return {}
                    raise error.InputError('The member you are trying to add is not a member of the channel')
            raise error.AccessError('You are not an owner of the flockr and cannot add owners')
    raise error.InputError('The channel you are trying to join does not exists')

def channel_removeowner(token, channel_id, u_id):
    caller_data = find_with_token(token)
    removed_person_data = find_with_uid(u_id)
    #Check if channel exists
    for channel in data['channels']:
        if channel_id == channel['id']:
            #Checks to see if the caller is an owner of the channel
                for owner in channel['owner_members']:
                    if caller_data[0] == owner['u_id']:
                        #Checks if the caller is an owner
                        if owner['u_id'] == u_id:
                            #if they are the last person in the channel, we raise an error. If not we remove them as owner
                            if len(channel['all_members']) == 1:
                                raise error.InputError('You are the only person in the channel, you cannot remove yourself as owner, please add another member')
                            elif len(channel['owner_members']) == 1:
                                raise error.InputError('You are the only owner in the channel, please make someone else owner before removing yourself')
                            else: 
                                remove_helper_func(channel_id, removed_person_data)
                                return {}
                        #If the caller is not removing himself, we check if the user is a member of the channel
                        for owner in channel['owner_members']:
                            if u_id == owner['u_id']:
                                remove_helper_func(channel_id, removed_person_data)
                                return {}
                        raise error.InputError('The member you are trying to remove is not an owner of the channel')
                raise error.AccessError('You are not an owner of the channel and cannot remove owners')
    raise error.InputError('The channel you are trying to access does not exists')


