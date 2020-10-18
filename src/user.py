from other import data, check_token
import error

def user_profile(token, u_id):
    return {
        'user': {
        	'u_id': 1,
        	'email': 'cs1531@cse.unsw.edu.au',
        	'name_first': 'Hayden',
        	'name_last': 'Jacobs',
        	'handle_str': 'hjacobs',
        },
    }

def user_profile_setname(token, name_first, name_last):
    return {
    }

def user_profile_setemail(token, email):
    return {
    }

def user_profile_sethandle(token, handle_str):
    #Check that the token is valid
    caller = check_token(token)

    handle_str_len = len(handle_str.strip())
    if handle_str_len > 20:
        raise InputError('User handle too long' )
    if handle_str_len < 3:
        raise InputError('User handle is too short')
    
    for user in data['users']:
        if handle_str == user['handle']


        
    
'''InputError when any of:
handle_str must be between 3 and 20 characters
handle is already used by another user'''
    return {
        
    }