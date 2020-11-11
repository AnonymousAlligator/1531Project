from other import data, check_token, find_with_uid, find_channel, is_member_check, is_owner_check
from remove_owner_helper import remove_helper_func, check_member_of_channel
import error

def channel_invite(token, channel_id, u_id):
    # Check that the token is valid
    inviter = check_token(token)

    # Check if user to be added exists within database
    invitee = find_with_uid(u_id)

    # Find the channel
    target_channel = find_channel(channel_id)

    # Check to see if inviter is part of that channel
    is_member = is_member_check(inviter['u_id'], target_channel)
    if not is_member:
        raise error.AccessError('You are not a member of the channel')
    # Check to see if invitee is part of that channel
    is_member = is_member_check(invitee['u_id'], target_channel)
    if is_member:
        raise error.InputError('User is already part of the channel')

    # Made it through all the checks so now we can add the invitee
    target_channel['all_members'].append({'u_id': invitee['u_id'], 
                                            'name_first': invitee['name_first'], 
                                            'name_last': invitee['name_last'],
                                            'profile_img_url': invitee['profile_img_url'],})
    # Also if permission_id is 1, then make them an owner
    if invitee['permission_id'] == 1:
        target_channel['owner_members'].append({'u_id': invitee['u_id'],
                                                'name_first': invitee['name_first'],
                                                'name_last': invitee['name_last'],
                                                'profile_img_url': invitee['profile_img_url'],})
    return {}

def channel_details(token, channel_id):
    # Check that the token is valid
    caller = check_token(token)

    # Find the channel
    target_channel = find_channel(channel_id)

    # Check to see if calling is part of that channel
    is_member = is_member_check(caller['u_id'], target_channel)
    # Access Error if the person inviting is not within the server
    if not is_member:
        raise error.AccessError('You are not part of the channel you want details about') 

    # Made it through all checks so now we start building the return
    channel_name = target_channel['name']
    # Append owner details
    channel_owners = []
    for owner in target_channel['owner_members']:
        channel_owners.append({'u_id': owner['u_id'],
                                'name_first': owner['name_first'],
                                'name_last': owner['name_last'], 
                                'profile_img_url' : owner['profile_img_url']})
    # Append member details
    channel_members = []
    for member in target_channel['all_members']:
        channel_members.append({'u_id': member['u_id'],
                                'name_first': member['name_first'],
                                'name_last': member['name_last'],
                                'profile_img_url' : member['profile_img_url']})
    
    return {'name': channel_name,
            'owner_members': channel_owners,
            'all_members': channel_members,
            }


def channel_messages(token, channel_id, start):
    # Check that the token is valid
    caller = check_token(token)
    
    # Find the channel
    target_channel = find_channel(channel_id)

    # Check to see if calling is part of that channel
    is_member = is_member_check(caller['u_id'], target_channel)
    # Access Error if the person inviting is not within the server
    if not is_member:
        raise error.AccessError('You are not part of the channel you want details about')
    
    # Made it through all checks so now we start building the return
    # Looping through the message data of the channel
    message_data = []
    number_of_messages = len(target_channel['messages'])
    message_number = start
    end = 0
    # Check if start is beyond range of messages
    if start > number_of_messages:
        raise error.InputError('The start value entered is older than all messages')
    # Check to see if start is the least recent message
    elif start == (number_of_messages - 1):
        message = target_channel['messages'][start]
        message_data.append(message)
        return {'messages': message_data, 
                'start': start, 
                'end': -1,}
    # We can iterate from start until either end or start + 50
    else:
        while (message_number < number_of_messages) and (end <= start + 49):
            message = target_channel['messages'][message_number]
            message_data.append(message)
            message_number += 1
            end += 1
        return {'messages': message_data,
                'start': start,
                'end': end,}

def channel_leave(token, channel_id):
    # Check that the token is valid
    caller = check_token(token)
    
    # Find the channel
    target_channel = find_channel(channel_id)

    # Check to see if inviter is part of that channel
    is_member = is_member_check(caller['u_id'], target_channel)
    # Access Error if the person calling is not within the server
    if not is_member:
        raise error.AccessError('You are not a member of the channel you are trying to leave')

    # Check if the user is the only owner but other members exist, input error if so
    is_owner = False
    for owner in target_channel['owner_members']:
        if owner['u_id'] == caller['u_id']:
            is_owner = True
            if len(target_channel['owner_members']) == 1 and len(target_channel['all_members']) != 1:
                raise error.InputError('Please make another member an owner before leaving')

    # If the user is an owner, remove them from the owner list
    if is_owner:
        for owner in target_channel['owner_members']:
            if owner['u_id'] == caller['u_id']:
                target_channel['owner_members'].remove(owner)
    # Navigate to the user entry in all members and remove them
    for user in target_channel['all_members']:
        if user['u_id'] == caller['u_id']:
            target_channel['all_members'].remove(user)
    # If there is now no one in the channel, delete the channel
    if len(target_channel['all_members']) == 0:
        for i, channel in enumerate(data['channels']):
            if channel['id'] == channel_id:
                del data['channels'][i]
    return {}

def channel_join(token, channel_id):
    # Check that the token is valid
    caller = check_token(token)

    # Find the channel
    target_channel = find_channel(channel_id)

    # If caller is flockr owner then add them to the channel and make them an owner
    if caller['permission_id'] == 1:
        target_channel['all_members'].append({'u_id': caller['u_id'], 
                                                'name_first': caller['name_first'], 
                                                'name_last': caller['name_last'],
                                                'profile_img_url': caller['profile_img_url']})
        target_channel['owner_members'].append({'u_id': caller['u_id'], 
                                                'name_first': caller['name_first'], 
                                                'name_last': caller['name_last'],
                                                'profile_img_url': caller['profile_img_url']})
        return {}

    # Otherwise, check to see if the channel they are joining is private
    if not target_channel['is_public']:
        raise error.AccessError('The channel you are trying to join is private')
    else:
        # Channel is public so we add their details into the channel list
        target_channel['all_members'].append({'u_id': caller['u_id'],
                                                'name_first': caller['name_first'],
                                                'name_last': caller['name_last'],
                                                'profile_img_url': caller['profile_img_url']})
        return {}

def channel_addowner(token, channel_id, u_id):
    # Check that the token is valid
    caller = check_token(token)
    # Checks that user is part of the flockr
    added_person = find_with_uid(u_id)

    # Find the channel
    target_channel = find_channel(channel_id)

    # Check to see if caller is an owner
    is_owner = is_owner_check(caller['u_id'], target_channel)
    # Access Error if the person calling is not an owner
    if not is_owner:
        raise error.AccessError('You are not an owner of the channel and cannot add owners')

    # We know the caller is an owner, now we see if they are adding themselves as owner
    if added_person['u_id'] == caller['u_id']:
        raise error.InputError('You are already an owner of this channel')

    # If we are here then we can proceed to check if the person to be promoted is in the channel
    is_member = is_member_check(added_person['u_id'], target_channel)
    # Input Error if the user doesn't exist
    if not is_member:
        raise error.InputError('User to be promoted is not in the channel')

    # We now check if the person to be promoted is already and owner
    is_owner = is_owner_check(added_person['u_id'], target_channel)
    if is_owner:
        raise error.InputError('The person you are trying promote is already an owner')

    # We can now promote the user to owner
    target_channel['owner_members'].append({'u_id' : added_person['u_id'],
                                            'name_first': added_person['name_first'],
                                            'name_last':added_person['name_last'],
                                            'profile_img_url': added_person['profile_img_url']})
    return {}

def channel_removeowner(token, channel_id, u_id):
    # Check that token is valied
    caller = check_token(token)

    # Check that user is part of flockr
    removed_person = find_with_uid(u_id)

    # Find the channel
    target_channel = find_channel(channel_id)

    # Check person to remove is part of channel
    is_member = is_member_check(caller['u_id'], target_channel)
    if not is_member:
        raise error.InputError('User to be removed is not in the channel')

    # Check to see if caller is an owner
    is_owner = is_owner_check(caller['u_id'], target_channel)
    # Access Error if the person calling is not an owner
    if not is_owner:
        raise error.AccessError('You are not an owner of the channel and cannot add owners')

    # Check to see if caller is a flockr owner
    if caller['permission_id'] == 1:
        is_owner = True

    # Access Error if the caller is not an owner
    if not is_owner:
        raise error.AccessError('You are not an owner of the channel and cannot remove owners')

    # Check to see if removed person is an owner
    is_owner = is_owner_check(removed_person['u_id'], target_channel)
    # Input Error if the person to be removed is not owner
    if not is_owner:
        raise error.InputError('Person to be demoted is not an owner')

    # Check to see if we are removing ourselves as owner
    if caller['u_id'] == removed_person['u_id']:
        # If we are the only person left in the channel then raise error
        if len(target_channel['all_members']) == 1:
            raise error.InputError('You are the only person in the channel, you cannot remove yourself as owner, please add another member')
        # If we are the only owner in the channel raise error to indicate a new owner must be assigned
        elif len(target_channel['owner_members']) == 1:
            raise error.InputError('You are the only owner in the channel, please make someone else owner before removing yourself')
        # Otherwise, we can remove self as owner
        else: 
            remove_helper_func(channel_id, removed_person)
            return {}
    # We can remove the person as owner
    remove_helper_func(channel_id, removed_person)
    return {}



