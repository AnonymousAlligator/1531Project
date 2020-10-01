from other import data
import error

def remove_helper_func(channel_id, removed_person):
    for channel in data['channels']:
        if channel_id == channel['id']:
            for owner in channel['owner_members']:
                if removed_person == owner['u_id']:
                    channel['owner_members'].remove(owner)
                    return {}
