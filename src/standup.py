from other import data, check_token, end_standup
import error
import threading
import time

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
    
    #Finds current time
    start_time = round(time.time())

    target_channel['standup']['is_standup'] = True 
    #calculates when it finishes
    target_channel['standup']['time_finish'] = start_time + length
    
    #Calls standup_send???
    return {'time_finish': end_time}

def standup_send(token, channel_id, message):
    

    t = threading.Timer(length, end_standup(target_channel))
    t.start()


