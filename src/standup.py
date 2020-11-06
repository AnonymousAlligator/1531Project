import time
import threading
import error
from other import data, check_token, end_standup

def standup_active(token, channel_id):
    # Check that the token is valid
    _ = check_token(token)

    # Find the channel
    target_channel = {}
    for channel in data['channels']:
        if channel_id == channel['id']:
            target_channel = channel
    # Input Error if the channel doesn't exist
    if target_channel == {}:
        #Input Error if the channel doesn't exist
        raise error.InputError('Channel does not exist')

    if target_channel['standup']['is_standup']:
        return {'is_active': True, 'time_finish': target_channel['standup']['time_finish']}
    return{'is_active': False, 'time_finish': None}

def standup_start(token, channel_id, length):
    # Check that the token is valid
    _ = check_token(token)

    # Find the channel
    target_channel = {}
    for channel in data['channels']:
        if channel_id == channel['id']:
            target_channel = channel
    # Input Error if the channel doesn't exist

    if target_channel == {}:
        raise error.InputError('Channel does not exist')

    #Finds current time and calculates when standup finishes
    start_time = round(time.time())
    end_time = start_time + length

    #Sets values on target_channel to indicate standup occuring
    target_channel['standup']['is_standup'] = True
    target_channel['standup']['time_finish'] = end_time

    # Begins thread that changes values in target channel to
    # indicate standup finished when timer is up
    thread = threading.Timer(length, end_standup(target_channel, token))
    thread.start()

    return {'time_finish': end_time}

def standup_send(token, channel_id, message):

    # get current utc time
    # TODO: check if we need utc time
    sent_time = time.time()

    caller = check_token(token)

    # check valid channel
    target_channel = {}
    for channel in data['channels']:
        if channel_id == channel['id']:
            target_channel = channel

    # InputError if invalid channel
    if target_channel == {}:
        raise error.InputError('Channel does not exist')

    # check if user is in channel
    is_member = False
    for member in target_channel['all_members']:
        if member['u_id'] == caller['u_id']:
            is_member = True

    # AccessError if user is not in channel
    if not is_member:
        raise error.AccessError('You are not a member of this channel.')

    # check the message length for issues
    if len(message) > 1000 or len(message) < 1 or len(message.strip()) < 1:
        raise error.InputError('Invalid message. Please shorten to less than 1000 characters.')

    # check for active standup
    standup = standup_active(token, channel_id)
    if standup['is_active']:
        raise error.InputError("There is already an active standup in channel")

    # update standup with new message if its still within timeframe
    if sent_time < standup['time_finish']:
        # TODO: check if we need to append user's deets
        target_channel['standup']['standup_messages'].append(message)
    else:
        raise error.AccessError(description="The standup has already ended")
