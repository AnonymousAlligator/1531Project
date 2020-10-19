from other import data, check_token, find_with_uid, email_check

import error

def user_profile(token, u_id):

    check_token(token)
    user_prof = {}

    user = find_with_uid(u_id)

    user_prof = {
        'u_id' : user['u_id'],
        'email': user['email'],
        'name_first':user['name_first'],
        'name_last': user['name_last'],
        'handle': user['handle'],
        }
    user_info = {}
    user_info['user'] = user_prof
    return user_info

def user_profile_setname(token, name_first, name_last):
    
    user = check_token(token)
    
    # check name_first is not between 1 and 50 characters
    if len(name_first) < 1 or len(name_first) > 50:
        raise error.InputError('First name must be between 1 and 50 characters')
    
    # check name_last is not between 1 and 50 characters
    if len(name_last) < 1 or len(name_last) > 50:
        raise error.InputError('Last name must be between 1 and 50 characters')
    
    user["name_first"] = name_first
    user["name_last"] = name_last

def user_profile_setemail(token, email):
    
    user = check_token(token)


    return {
    }

def user_profile_sethandle(token, handle_str):
    #Check that the token is valid
    caller = check_token(token)

    handle_str_len = len(handle_str.strip())
    if handle_str_len > 20:
        raise error.InputError('User handle too long')
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
