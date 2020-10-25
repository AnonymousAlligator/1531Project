from other import data, check_token, find_with_uid
import re 
import error

def user_profile(token, u_id):

    check_token(token)
    user = find_with_uid(u_id)
    user_info = {
        'u_id' : user['u_id'],
        'email': user['email'],
        'name_first':user['name_first'],
        'name_last': user['name_last'],
        'handle_str': user['handle_str'],
        }
    return {'user': user_info}


def user_profile_setname(token, name_first, name_last):
    
    caller = check_token(token)

    # remove trailing and leading whitespaces
    fname = name_first.strip()
    lname = name_last.strip()
    
    # check name_first is between 1 and 50 characters
    if len(fname) < 1 or len(fname) > 50:
        raise error.InputError('First name must be between 1 and 50 characters')
    
    # check name_last is between 1 and 50 characters
    if len(lname) < 1 or len(lname) > 50:
        raise error.InputError('Last name must be between 1 and 50 characters')
    
    caller["name_first"] = fname
    caller["name_last"] = lname

    return {}
    

def user_profile_setemail(token, email):
    
    caller = check_token(token)
    
    # remove trailing and leading whitespaces from input
    email = email.strip()

    # check for valid email
    email_match = r'^\w+([\.-]?\w+)*@\w([\.-]?\w+)*(\.\w{2,3})+$'
    if not re.search(email_match, email): # If it returns FALSE
        raise error.InputError('Entered email is not valid')

    # check for existing email
    for user in data['users']:
        if user['email'] == email:
            raise error.InputError("Email already taken by another registered user")

    caller["email"] = email
    return {}

def user_profile_sethandle(token, handle_str):
    #Check that the token is valid
    caller = check_token(token)

    # remove trailing and leading whitespaces from input
    handle_str = handle_str.strip()

    handle_str_len = len(handle_str.strip())
    if handle_str_len > 20:
        raise error.InputError('User handle too long')
    if handle_str_len < 3:
        raise error.InputError('User handle is too short')

    #check that the handle is not already used
    handle_used = False
    for user in data['users']:
        if handle_str == user['handle_str']:
            handle_used = True
    if handle_used:
        raise error.InputError('User handle is already used by another user')

    #Sets handle
    caller['handle_str'] = handle_str

    return {}