from other import data, check_token
import error
import datetime
import threading

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

    # Check to see if caller is part of that channel
    is_member = False
    for member in target_channel['all_members']:
        if member['u_id'] == caller['u_id']:
            is_member = True
    # Access Error if the person inviting is not within the server
    if not is_member:
        raise error.AccessError('You are not part of the channel you want to send messages to')

    # Check the message length for issues
    if len(message) > 1000 or len(message) < 1 or len(message.strip()) < 1:
        raise error.InputError('The message you are sending is over 1000 characters')

    # message gets added to the channel's message key
    if len(data['messages']) == 0:
        message_id = 0
    else:
        message_id = data['messages'][0]['message_id'] + 1
    time_created = round((datetime.datetime.now()).timestamp())
    channel_message = {'message_id': message_id,
                    'u_id': caller['u_id'],
                    'message': message,
                    'time_created': time_created}
    target_channel['messages'].insert(0, channel_message)

    # adding data to messages for easier searching
    message_data = {'message_id': message_id,
                    'u_id': caller['u_id'],
                    'message': message,
                    'time_created': time_created,
                    'channel_id' : channel_id,}
    data['messages'].insert(0, message_data)
    return {
        'message_id': message_id
    }

def message_remove(token, message_id):
    # Check that the token is valid
    caller = check_token(token)
    
    # Find the message in the message field of data
    target_message = {}
    for message in data['messages']:
        if message_id == message['message_id']:
            target_message = message
    # If no target is returned then the message no longer exits, InputError
    if target_message == {}:
        raise error.InputError('Message no longer exists')

    # Find the channel the message is in
    target_channel = {}
    for channel in data['channels']:
        if target_message['channel_id'] == channel['id']:
            target_channel = channel

    # Check to see if the caller has the right to remove the message
    is_allowed = False
    # 1) Caller u_id == target_message u_id
    if caller['u_id'] == target_message['u_id']:
        is_allowed = True

    # 2) Caller is channel owner
    if not is_allowed:
        for owner in target_channel['owner_members']:
            if owner['u_id'] == caller['u_id']:
                is_allowed = True

    # 3) Caller is flockr owner
    if not is_allowed:
        if caller['permission_id'] == 1:
            is_allowed = True

    # If permission is found then remove the message, else access error
    if is_allowed:
        for i, message in enumerate(target_channel['messages']):
            if message['message_id'] == target_message['message_id']:
                del target_channel['messages'][i]
        for i, message in enumerate(data['messages']):
            if message_id == message['message_id']:
                del data['messages'][i]
        return {}
    raise error.AccessError('You are not allowed to remove the message')

def message_edit(token, message_id, message):

    user = check_token(token)

    # Find the message in the message field of data
    target_message = {}
    for message_value in data['messages']:
        if message_id == message_value['message_id']:
            target_message = message_value
    # If no target is returned then the message no longer exits, InputError
    if target_message == {}:
        raise error.InputError('Message does not exist')

    # Find the channel the message is in
    target_channel = {}
    channel_index = 0
    for channel in data['channels']:
        if target_message['channel_id'] == channel['id']:
            target_channel = channel
            break
        channel_index += 1

    # Check to see if the caller has the right to remove the message
    is_allowed = False
    # 1) Caller u_id == target_message u_id
    if user['u_id'] == target_message['u_id']:
        is_allowed = True

    # 2) Caller is channel owner
    if not is_allowed:
        for owner in target_channel['owner_members']:
            if owner['u_id'] == user['u_id']:
                is_allowed = True

    # 3) Caller is flockr owner
    if not is_allowed:
        if user['permission_id'] == 1:
            is_allowed = True

    if not is_allowed:
        raise error.AccessError('You do not have permission to edit message')
    
    # If the message parsed in all white space or empty, then remove
    message_length = len(message.strip())
    if message_length == 0:
        message_remove(token, message_id)
        return {}
    else:
        channel['messages'][channel_index]['message'] = message

    for messages in data['messages']:
        if message_id == messages['message_id']:
            messages['message'] = message
            return {}

def message_sendlater(token, channel_id, message, time_sent):
    # Check that the token is valid
    caller = check_token(token)

    # Capture the current time asap
    current_time = (datetime.datetime.now()).timestamp()

    # Find the channel
    target_channel = {}
    for channel in data['channels']:
        if channel_id == channel['id']:
            target_channel = channel
    # Input Error if the channel doesn't exist
    if target_channel == {}:
        #Input Error if the channel doesn't exist
        raise error.InputError('Channel does not exist')

    # Check to see if caller is part of that channel
    is_member = False
    for member in target_channel['all_members']:
        if member['u_id'] == caller['u_id']:
            is_member = True
    # Access Error if the person inviting is not within the server
    if not is_member:
        raise error.AccessError('You are not part of the channel you want to send messages to')

    # Check the message length for issues
    if len(message) > 1000 or len(message) < 1 or len(message.strip()) < 1:
        raise error.InputError('The message you are sending is over 1000 characters')

    # Check the time is not from before current
    if (time_sent - current_time) < 0:
        raise error.InputError('Trying to send message in the past')

    delay = time_sent - current_time
    threading.Timer(delay, send_message, kwargs={'caller':caller, 'message':message, 'target_channel':target_channel, 'channel_id':channel_id}).start()

def send_message(caller, message, target_channel, channel_id):
    # message gets added to the channel's message key
    if len(data['messages']) == 0:
        message_id = 0
    else:
        message_id = data['messages'][0]['message_id'] + 1
    time_created = round((datetime.datetime.now()).timestamp())
    channel_message = {'message_id': message_id,
                    'u_id': caller['u_id'],
                    'message': message,
                    'time_created': time_created}
    target_channel['messages'].insert(0, channel_message)

    # adding data to messages for easier searching
    message_data = {'message_id': message_id,
                    'u_id': caller['u_id'],
                    'message': message,
                    'time_created': time_created,
                    'channel_id' : channel_id,}
    data['messages'].insert(0, message_data)
    return {
        'message_id': message_id
    }
