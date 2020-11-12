import time
import threading
import error
from other import data, check_token, find_channel, is_member_check
from message import send_message

def standup_active(token, channel_id):
    # Check that the token is valid
    caller = check_token(token)

    # Find the channel
    target_channel = find_channel(channel_id)

    # Check to see if caller is part of that channel
    is_member = is_member_check(caller['u_id'], target_channel)
    if not is_member:
        raise error.AccessError('You are not part of the channel')

    # check for active standup
    if target_channel['standup']['is_standup']:
        return {'is_active': True, 'time_finish': target_channel['standup']['time_finish']}
    return{'is_active': False, 'time_finish': None}

def standup_start(token, channel_id, length):
    # Check that the token is valid
    caller = check_token(token)

    # Find the channel
    target_channel = find_channel(channel_id)

    # Check to see if caller is part of that channe
    is_member = is_member_check(caller['u_id'], target_channel)
    if not is_member:
        raise error.AccessError('You are not part of the channel')

    # check for active standup
    standup = standup_active(token, channel_id)
    if standup['is_active'] is True:
        raise error.InputError("There is already an active standup in channel")

    # finds current time and calculates when standup finishes
    start_time = round(time.time())
    end_time = start_time + length

    # sets values on target_channel to indicate standup occuring
    target_channel['standup']['is_standup'] = True
    target_channel['standup']['time_finish'] = end_time
    target_channel['standup']['standup_messages'] = []

    # make new thread
    threading.Thread(target = end_standup, args = (target_channel, token, length)).start()

    return {'time_finish': end_time}

def standup_send(token, channel_id, message):

    # check for valid token
    caller = check_token(token)

    # check valid channel
    target_channel = find_channel(channel_id)

    # check if user is in channel
    is_member = is_member_check(caller['u_id'], target_channel)
    if not is_member:
        raise error.AccessError('You are not part of the channel')

    # check the message length for issues
    if len(message) > 1000 or len(message) < 1 or len(message.strip()) < 1:
        raise error.InputError('Invalid message. Please shorten to less than 1000 characters.')

    # check for active standup
    standup = standup_active(token, channel_id)
    if standup['is_active'] is False:
        raise error.InputError("There is already an active standup in channel")

    # throw error if message is user trying to start standup
    if message.startswith('/standup'):
        raise error.InputError("There is already an active standup in channel")

    # update standup with message and user's details
    target_channel['standup']['standup_messages'].append(caller['name_first'] + ': ' + message)
    return {}

def end_standup(target_channel, token, length):

    time.sleep(length)

    # update channel with end standup
    target_channel['standup']['is_standup'] = False
    target_channel['standup']['time_finish'] = None

    # join all messages into standup_messages separated by new line
    standup_messages = '\n'.join(target_channel['standup']['standup_messages'])

    # get user
    caller = check_token(token)

    # send standup_messages from the user who called the standup
    send_message(caller, standup_messages, target_channel, target_channel['id'])

    # clear messages from standup buffer
    for old_message in target_channel['standup']['standup_messages']:
        target_channel['standup']['standup_messages'].remove(old_message)
