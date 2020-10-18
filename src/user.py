from other import data, check_token, find_with_uid

import error

def user_profile(token, u_id):
    check_token(token)
    user_profile = {}

    user = find_with_uid(u_id)

    user_profile = {
        'u_id' : user['u_id'],
        'email': user['email'], 
        'name_first':user['name_first'], 
        'name_last': user['name_last'], 
        'handle': user['handle'],
        }

    return user_profile

    '''
    return {
        'user': {
            'u_id': 1,
            'email': 'cs1531@cse.unsw.edu.au',
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
            'handle': 'jacobs',
        },
    }
    '''

def user_profile_setname(token, name_first, name_last):
    pass
    return {
    }

def user_profile_setemail(token, email):
    pass
    return {
    }

def user_profile_sethandle(token, handle_str):
    #Check that the token is valid
    caller = check_token(token)

    handle_str_len = len(handle_str.strip())
    if handle_str_len > 20:
        raise error.InputError('User handle too long' )
    if handle_str_len < 3:
        raise error.InputError('User handle is too short')

    #check that the handle is not already used
    handle_used = False
    for user in data['users']:
        if handle_str == user['handle']:
            handle_used = True
    if handle_used:
        raise error.InputError('User handle is already used by another user')

    #Sets handle
    caller['handle'] = handle_str

    return {}