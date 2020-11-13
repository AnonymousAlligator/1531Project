from other import data, check_token, find_with_uid, find_channel, is_member_check, is_owner_check, find_message_in_messages
import error
import datetime
import threading

def message_send(token, channel_id, message):
    # Check that the token is valid
    caller = check_token(token)

    # Find the channel
    target_channel = find_channel(channel_id)

    # Check to see if caller is part of that channel
    is_member = is_member_check(caller['u_id'], target_channel)
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
                    'time_created': time_created,
                    'reacts' : [],
                    'is_pinned': False,
                    }
    target_channel['messages'].insert(0, channel_message)

    # adding data to messages for easier searching
    message_data = {'message_id': message_id,
                    'u_id': caller['u_id'],
                    'message': message,
                    'time_created': time_created,
                    'channel_id' : channel_id,
                    'reacts' : [],
                    'is_pinned': False,
                    }
    data['messages'].insert(0, message_data)
    return {
        'message_id': message_id
    }

def message_remove(token, message_id):
    # Check that the token is valid
    caller = check_token(token)

    # Find the message in the message field of data
    target_message = find_message_in_messages(message_id)

    # Find the channel the message is in
    target_channel = find_channel(target_message['channel_id'])

    # Check to see if the caller has the right to remove the message
    is_allowed = False
    # 1) Caller u_id == target_message u_id
    if caller['u_id'] == target_message['u_id']:
        is_allowed = True

    # 2) Caller is channel owner
    if not is_allowed:
        is_allowed = is_owner_check(caller['u_id'], target_channel)

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

    caller = check_token(token)

    # Find the message in the message field of data
    target_message = find_message_in_messages(message_id)

    # Find the channel the message is in
    target_channel = find_channel(target_message['channel_id'])

    # Check to see if the caller has the right to remove the message
    is_allowed = False
    # 1) Caller u_id == target_message u_id
    if caller['u_id'] == target_message['u_id']:
        is_allowed = True

    # 2) Caller is channel owner
    if not is_allowed:
        is_allowed = is_owner_check(caller['u_id'], target_channel)

    # 3) Caller is flockr owner
    if not is_allowed:
        if caller['permission_id'] == 1:
            is_allowed = True

    if not is_allowed:
        raise error.AccessError('You do not have permission to edit message')

    # If the message parsed in all white space or empty, then remove
    message_length = len(message.strip())
    if message_length == 0:
        message_remove(token, message_id)
        return {}
    for message_data in target_channel['messages']:
        if message_id == message_data['message_id']:
            message_data['message'] = message
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
    target_channel = find_channel(channel_id)

    # Check to see if caller is part of that channel
    is_member = is_member_check(caller['u_id'], target_channel)
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
    threading.Timer(delay, send_message, kwargs={'caller':caller,
                                                    'message':message,
                                                    'target_channel':target_channel,
                                                    'channel_id':channel_id}).start()

def message_react(token, message_id, react_id):
    # Make sure react_id is valid
    thumbs_up = 1
    if react_id != thumbs_up:
        raise error.InputError('Invalid react_id')

    # check for valid user
    user = check_token(token)

    # Find the message in the message field of data
    target_message = find_message_in_messages(message_id)

    # Find the channel the message is in
    target_channel = {}
    channel_index = 0
    for channel in data['channels']:
        if target_message['channel_id'] == channel['id']:
            target_channel = channel
            break
        channel_index += 1
    # Make sure the user is in the channel
    channel_check = 0
    for members in target_channel['all_members']:
        if user['u_id'] == members['u_id']:
            channel_check += 1

    # InputError if channel does not exist
    if target_channel == {}:
        raise error.InputError('You are trying to access an invalid channel')

    append_flag = 0
    # Add react to u_id in messages for react type if react is not found
    for reacts in target_message['reacts']:
        if react_id == reacts['react_id']:
            reacts['u_ids'].append(user['u_id'])
            append_flag += 1
        if append_flag == 1:
            break
        else:
            target_message['reacts'].append({'react_id' : react_id,
                            'u_ids' : [user['u_id'],],
                            'is_this_user_reacted' : False,
                            })
    append_flag = 0
    # update channel['messages'] with react data as well
    for channel_message in target_channel['messages']:
        if channel_message['message_id'] == target_message['message_id']:
            for reacts in channel_message['reacts']:
                if react_id == reacts['react_id']:
                    reacts['u_ids'].append(user['u_id'])
                    append_flag += 1
            if append_flag == 1:
                break
            else:       
                channel_message['reacts'].append({'react_id' : react_id,
                            'u_ids' : [user['u_id'],],
                            'is_this_user_reacted' : False,
                            })
    return {}

def message_unreact(token, message_id, react_id):
    # Make sure react_id is valid
    thumbs_up = 1
    if react_id != thumbs_up:
        raise error.InputError('Invalid react_id')

    # check for valid user
    user = check_token(token)

    # Find the message in the message field of data
    target_message = {}
    for message_value in data['messages']:
        if message_id == message_value['message_id']:
            target_message = message_value
    # InputError if message doesnt exist
    if target_message == {}:
        raise error.InputError('Message does not exist')
        
    # Find the channel the message is in
    target_channel = find_channel(target_message['channel_id'])

    # Remove u_id in messages for react type 
    for reacts in target_message['reacts']:
        if react_id == reacts['react_id']:
            reacts['u_ids'].remove(user['u_id'])

    # update channel['messages'] with react data as well
    for channel_message in target_channel['messages']:
        if channel_message['message_id'] == target_message['message_id']:
            for reacts in channel_message['reacts']:
                if react_id == reacts['react_id']:
                    reacts['u_ids'].remove(user['u_id'])
    return {}

def message_pin(token, message_id):

    # check for valid user
    caller = check_token(token)

    # Find the message in the message field of data
    target_message = find_message_in_messages(message_id)
    if target_message['is_pinned']:
        raise error.InputError('Message is already pinned')

    # Find the channel the message is in
    target_channel = find_channel(target_message['channel_id'])

    # Check to see if caller is part of that channel
    is_member = is_member_check(caller['u_id'], target_channel)
    if not is_member:
        raise error.AccessError('You are not part of this channel.')

    # check user is owner
    is_allowed = is_owner_check(caller['u_id'], target_channel)
    if not is_allowed:
        raise error.AccessError('You do not have permission to pin message')

    for message in target_channel['messages']:
        if message['message_id'] == message_id:
            message['is_pinned'] = True
    for message in data['messages']:
        if message_id == message['message_id']:
            message['is_pinned'] = True
            return {}

def message_unpin(token, message_id):

    # check for valid user
    caller = check_token(token)

    # check for valid message_id
    target_message = find_message_in_messages(message_id)
    if not target_message['is_pinned']:
        raise error.InputError('Message is not pinned')

    # Find the channel the message is in
    target_channel = find_channel(target_message['channel_id'])

    # Check to see if caller is part of that channel
    is_member = is_member_check(caller['u_id'], target_channel)
    if not is_member:
        raise error.AccessError('You are not part of this channel.')

    # check user is owner
    is_allowed = is_owner_check(caller['u_id'], target_channel)
    if not is_allowed:
        raise error.AccessError('You do not have permission to unpin message')
    
    for message in target_channel['messages']:
        if message['message_id'] == message_id:
            message['is_pinned'] = False
    for message in data['messages']:
        if message_id == message['message_id']:
            message['is_pinned'] = False
            return {}

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
                    'time_created': time_created,
                    'reacts' : [],}
    target_channel['messages'].insert(0, channel_message)

    # adding data to messages for easier searching
    message_data = {'message_id': message_id,
                    'u_id': caller['u_id'],
                    'message': message,
                    'time_created': time_created,
                    'channel_id' : channel_id,
                    'reacts' : [],}
    data['messages'].insert(0, message_data)
    return {
        'message_id': message_id
    }
