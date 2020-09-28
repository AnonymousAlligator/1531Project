from other import data
import error

def channel_invite(token, channel_id, u_id):
    return {
    }

def channel_details(token, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages(token, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave(token, channel_id):
    return {
    }

def channel_join(token, channel_id):
    # Check for if the channel_id is valid
    for channels in data['channels']:
        # If we find the channel check if it is private
        if channel_id == channels['id']:
            # Access error if the channel is private
            if channels['is_public'] == False:
                raise error.AccessError('The channel you are trying to join is private')
            else:
                # Channel is public so we search for the user's details..
                for users in data['users']:
                    # And add their details into the channel list
                    if token == users['token']:
                        channels['all_members'].append({'u_id': users['u_id'], 'name_first': users['name_first'], 'name_last': users['name_last']})
                        return {}
        else:
            raise error.InputError('The channel you are trying to join does not exist')
    return {
    }

def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }