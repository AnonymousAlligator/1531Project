from other import data, check_token, end_standup
import error
import threading
import time

def standup_active(token, channel_id):
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
    if not is_member:
        raise error.AccessError('You are not part of the channel')

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
    
    #Begins thread that changes values in target channel to indicate standup finished when timer is up
    t = threading.Timer(length, end_standup, kwargs={'target_channel':target_channel})
    t.start()

    return {'time_finish': end_time}

def standup_send(token, channel_id, message):
    pass




