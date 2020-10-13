from other import data, check_token
import error
import datetime

def message_send(token, channel_id, message):
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

    # Check to see if inviter is part of that channel
    is_member = False
    for member in target_channel['all_members']:
        if member['u_id'] == caller['u_id']:
            is_member = True
    # Access Error if the person inviting is not within the server
    if is_member:
        raise error.AccessError('You are not part of the channel you want details about')

    # Check the message length
    if len(message) > 1000:
        raise error.InputError('The message you are sending is over 1000 characters')

    # message gets added to the channel's message key
    message_id = len(data['messages'])
    message_data = {message_id, caller['u_id'], message, datetime.datetime.now(),}
    target_channel['messages'].insert(0, message_data)

    # message id, channel id and u_id get added to the messages key (used in removal)
    data['messages'].insert(0, {'u_id': caller['u_id'], 'message_id': message_id, 'channel_id': channel_id})
    return {
        'message_id': message_id
    }

def message_remove(token, message_id):
    # Check that the token is valid
    caller = check_token(token)

    # Find the channel the message is in by searching the data key
    target_message = {}
    for message in data['messages']
        if message_id == message['message_id']:
            target_message = message
    # If no target is returned then the message no longer exits, InputError
    if target_message == {}:
        raise error.InputError('Message no longer exists')

    # Check to see if the caller's u_id matches that of the sender or if the caller is owner of channel/flockr
    if caller['u_id'] == target_message['u_id'] or is_owner
    return {
    }

def message_edit(token, message_id, message):
    return {
    }