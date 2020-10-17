def user_profile(token, u_id):
    
    data.check_token(token)
    
    found_user = 0
    for user in data['users']:
        if user['u_id'] == u_id:
            found_user = 1
   
    if found_user == 0:
        raise InputError('User doesnt exist')

    user_info = {
        'u_id' : user['u_id'],
        'email': user['email'],
        'name_first': user['first_name'],
        'name_last': user['second_name'],
        'handle_str': user['handle'],
    }

    return user_info

def user_profile_setname(token, name_first, name_last):
    return {
    }

def user_profile_setemail(token, email):
    return {
    }

def user_profile_sethandle(token, handle_str):
    return {
    }