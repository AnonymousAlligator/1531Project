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

def message_react(token, message_id, react_id):
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
    target_channel = {}
    channel_index = 0
    for channel in data['channels']:
        if target_message['channel_id'] == channel['id']:
            target_channel = channel
            break
        channel_index += 1
    # InputError if channel does not exist
    if target_channel == {}:
        raise error.InputError('You are trying to access an invalid channel')

    for reacts in target_message['reacts']:
        # If react is found check if user has reacted before
        if reacts['u_ids'] == user['u_id'] and reacts['react_id'] == react_id:
            # raise error if already reacted
            if reacts['is_this_user_reacted'] == True:
                raise error.AccessError('Message already contains active react')
            # If react is not active make react active
            #TODO dynamically generate is_this_user_reacted?
            reacts['is_this_user_reacted'] = True
            return {}

    # Add react dictionary in messages for react type if react is not found
    target_message['reacts'].append({'react_id' : react_id,
                            'u_ids' : user['u_id'],
                            'is_this_user_reacted' : True,
                            })

    # update channel['messages'] with react data as well
    for channel_message in target_channel['messages']:
        if channel_message['message_id'] == target_message['message_id']:
            channel_message['reacts'].append({'react_id' : react_id,
                            'u_ids' : user['u_id'],
                            'is_this_user_reacted' : True,
                            })

def message_unreact(token, message_id, react_id):

    # check for valid react_id
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
    # InputError if message does not exist
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
    # InputError if channel does not exist
    if target_channel == {}:
        raise error.InputError('You are trying to access an invalid channel')

    # InputError if user is not part of channel
    is_member = False
    for member in target_channel['all_members']:
        if member['u_id'] == user['u_id']:
            is_member = True
    if not is_member:
        raise error.InputError('You can only react to messages in a channel you have joined.')

    # update react in channel['messages']
    for channel_message in target_channel['messages']:
        if channel_message['message_id'] == target_message['message_id']:
            for reacts in channel_message['reacts']:                
                if reacts['u_ids'] == user['u_id'] and reacts['react_id'] == react_id:
                    # if react is found check if user has reacted before
                    if reacts['is_this_user_reacted'] == False:
                        #  if False raise AccessError
                        raise error.AccessError('Message it not active react')
                    # If react is not active make react active
                    reacts['is_this_user_reacted'] = False

    # Find message to change react for person
    for reacts in target_message['reacts']:
        if reacts['u_ids'] == user['u_id'] and reacts['react_id'] == react_id:
        # if react is found check if user has reacted before
            if reacts['is_this_user_reacted'] == False:
                #  if False raise AccessError
                raise error.AccessError('Message it not active react')
            # If react is not active make react active
            reacts['is_this_user_reacted'] = False

def message_pin(token, message_id):

    user = check_token(token)

    # Find the message in the message field of data
    target_message = {}
    for message_value in data['messages']:
        if message_id == message_value['message_id']:
            target_message = message_value
    # If no target is returned then the message no longer exits, InputError
    if target_message == {}:
        raise error.InputError('Message does not exist')
    # If message is pinned already, InputError
    if target_message['is_pinned'] == True:
        raise error.InputError('Message is already pinned')
    
    # Find the channel the message is in
    target_channel = {}
    channel_index = 0
    for channel in data['channels']:
        if target_message['channel_id'] == channel['id']:
            target_channel = channel
            break
        channel_index += 1
    # Check if caller is within the channel
    in_channel = False
    for member in target_channel['all_members']:
        if user['u_id'] == member['u_id']:
            in_channel = True

    if not in_channel:
       raise error.AccessError('You are not in this channel') 
    # Check to see if the caller has the right to pin the message
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
        raise error.AccessError('You do not have permission to pin message')

    channel['messages'][channel_index]['is_pinned'] = True

    for messages in data['messages']:
        if message_id == messages['message_id']:
            messages['is_pinned'] = True
            return {}

def message_unpin(token, message_id):

    user = check_token(token)

    # Find the message in the message field of data
    target_message = {}
    for message_value in data['messages']:
        if message_id == message_value['message_id']:
            target_message = message_value
    # If no target is returned then the message no longer exits, InputError
    if target_message == {}:
        raise error.InputError('Message does not exist')
    # If message is pinned already, InputError
    if target_message['is_pinned'] == False:
        raise error.InputError('Message is already pinned')
    
    # Find the channel the message is in
    target_channel = {}
    channel_index = 0
    for channel in data['channels']:
        if target_message['channel_id'] == channel['id']:
            target_channel = channel
            break
        channel_index += 1
    # Check if caller is within the channel
    in_channel = False
    for member in target_channel['all_members']:
        if user['u_id'] == member['u_id']:
            in_channel = True

    if not in_channel:
       raise error.AccessError('You are not in this channel') 
    # Check to see if the caller has the right to pin the message
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
        raise error.AccessError('You do not have permission to pin message')

    channel['messages'][channel_index]['is_pinned'] = False

    for messages in data['messages']:
        if message_id == messages['message_id']:
            messages['is_pinned'] = False
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

