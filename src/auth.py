import re 
from other import data, check_token, email_check
from error import InputError, AccessError

def auth_login(email, password):
    
    flag = 0
    for user in data['users']:
        if user['email'] == email:
            found_user = user
            flag = 1
        if user['token'] != "False":
            raise InputError('You are already logged in')

    if flag == 0:
        raise InputError('Email has not been registered previously')
    
    if password != found_user['password']:
        raise InputError('Password entered is not correct')
    
    token = email 
    user['token'] = token
    return {
        'u_id': found_user['u_id'], 'token': token,
    }

def auth_logout(token):
    try:
        user = check_token(token)
    except:
        return {'is_success': False}
    
    flag = False
       
    if user['token'] == token:
        for info in data['users']:
            if info == user:
                flag = True
                user['token'] = "False"
                break
    return {'is_success': flag}

def auth_register(email, password, name_first, name_last):
    
    # Password needs to be at least 6 characters long
    if len(password) < 6:
        raise InputError('Password entered is less than 6 characters long')

    if not email_check(email): # If it returns FALSE
        raise InputError('Entered email is not valid')

    first_name_length = len(name_first.strip())
    last_name_length = len(name_last.strip())

    # First name doesn't contain at least 1 character
    if first_name_length < 1:
        raise InputError('First name is less than 1 character long')

    # First name contains more than 50 characters
    if first_name_length > 50:
        raise InputError('First name is more than 50 characters long')

    if last_name_length < 1:
        raise InputError('Last name is less than 1 character long')

    if last_name_length > 50: 
        raise InputError('Last name is more than 50 characters long')

    # Check if email already registered
    for registered_user in data['users']:
        if registered_user['email'] == email:
            raise InputError('Email already taken by another registered user')

    u_id = len(data['users']) # checks the number of people in the users database to establish the u_id

    data['users'].append({
        'u_id': u_id,
        'email': email, 
        'name_first':name_first, 
        'name_last': name_last, 
        'password': password, 
        'handle': name_first+name_last, 
        'token': email,
    })

    return {
        'u_id': u_id,
        'token': email,
    }

