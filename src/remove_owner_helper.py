from other import data
import error

def remove_helper_func(channel_id, removed_person):
    for channel in data['channels']:
        if channel_id == channel['id']:
            for owner in channel['owner_members']:
                if removed_person['u_id'] == owner['u_id']:
                    channel['owner_members'].remove(owner)
                    return {}


def find_with_uid(u_id):
    for user in data['users']:
        if u_id == user['u_id']:
            return(user)
    # If we are here then the token was invalid
    raise error.AccessError('The user ID does not exist')

def check_member_of_channel(removed_person):
    for channel in data['channels']:
        for member in channel['all_members']:
            if removed_person['u_id'] == member['u_id']:
                return(member)
        raise error.InputError('The person you are trying to add is not a member of this channel')