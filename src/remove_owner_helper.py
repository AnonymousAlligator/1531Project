from other import data
import error

def remove_helper_func(channel_id, removed_person_data):
    for channel in data['channels']:
        if channel_id == channel['id']:
            for owner in channel['owner_members']:
                if removed_person_data[0] == owner['u_id']:
                    channel['owner_members'].remove(owner)
                    return {}


def find_with_token(token):
    for user in data['users']:
        if token == user['token']:
            name_data = user['u_id'], user['name_first'], user['name_last']
            return(name_data)
    # If we are here then the token was invalid
    raise error.AccessError('Invalid token recieved')

def find_with_uid(u_id):
    for user in data['users']:
        if u_id == user['u_id']:
            name_data = user['u_id'], user['name_first'], user['name_last']
            return(name_data)
    # If we are here then the token was invalid
    raise error.AccessError('Invalid token recieved')