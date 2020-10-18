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
    for message in data['messages']:
        if message_id == message['message_id']:
            target_message = message
    # If no target is returned then the message no longer exits, InputError
    if target_message == {}:
        raise error.InputError('Message no longer exists')

    # Check to see if the caller's u_id matches that of the sender or if the caller is owner of channel/flockr
    if caller['u_id'] == target_message['u_id']:
        pass
    return {
    }

def message_edit(token, message_id, message):
    
    user = data.check_token(token)

    info_message = None
    # Searches through all the messages in all the existing channels channel by channel
    for channel in data['channels']:
        total_messages = len(channel['messages'])
        for nth_message in range(0, total_messages):
            # If the message is found inside current channel 
            if channel['messages'][nth_message]['message_id'] == message_id:
                info_message = {'nth_message': nth_message,
                                'message': channel['messages'][nth_message],
                                'channel_id': channel['channel_id']}

    # If the message cannot be found across all the channels, info_message stays equal to none
    
    returned_channel = None
    for channel in data['channel']:
        if channel['channel_id'] == info_message['channel_id']:
            returned_channel = channel # All channel info stored in here
            break

    message_sender_uid = info_message['message']['u_id']

    # If user who sent request didn't send the message, is not a channel owner, or is not a slackr owner
    ############ NEED TO DISCUSS HOW WE WANT TO SET THE PID STUFF UP ################
    if message_sender_uid != user['u_id'] and user['p_id'] == PID_MEMBER and channel.get(user['u_id'] != 1):
        raise AccessError('You do not have permission to edit message')

    new_message_length = len(message)
    # Finds the message and edits it
    for i in range(0, new_message_length):
        if message[i] != ' ':
            channel['messages'][nth_message]['message'] = message # Edits the message
            return {}

    # Removes the old message
    message_remove(token, message_id)
    return {}