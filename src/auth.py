import re 
from other import data, check_token
from error import InputError, AccessError
import random
import string
import hashlib
import jwt

def auth_login(email, password):
    
    password = hashlib.sha256(password.encode()).hexdigest()

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
    
    token = jwt.encode({found_user['u_id']:'u_id'}, 'jekfwbdkbwkf', algorithm='HS256').decode('utf-8')

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

    email_match = r'^\w+([\.-]?\w+)*@\w([\.-]?\w+)*(\.\w{2,3})+$'
    if not re.search(email_match, email): # If it returns FALSE
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

    initial_handle = (name_first + name_last).lower()
    if len(initial_handle) >= 20:
        initial_handle = initial_handle[:20]

    middle_handle = initial_handle
    
    for user in data['users']:
        if user['handle'] == initial_handle:
            middle_handle = initial_handle
            num_suffix = 1
            for user in data['users']:
                if user['handle'] == middle_handle:
                    middle_handle = initial_handle + str(num_suffix)
                    num_suffix = num_suffix + 1
            
    handle = middle_handle  

    if len(handle) > 20:
        handle = ''.join(random.choice(string.ascii_lowercase) for _ in range(20))   

    password = hashlib.sha256(password.encode()).hexdigest()
    token = jwt.encode({'u_id': u_id}, 'jekfwbdkbwkf', algorithm='HS256').decode('utf-8')          

    data['users'].append({
        'u_id': u_id,
        'email': email, 
        'name_first':name_first, 
        'name_last': name_last, 
        'password': password, 
        'handle': handle, 
        'token': token,
    })

    return {
        'u_id': u_id,
        'token': token,
        'handle': handle,
        'password': password
    }


valid_user = auth_register("1st_email@valid.com", "potato321", "abcdefghij", "klmnopqrst")
valid_user2 = auth_register("2nd_email@valid.com", "wdnqwiu1", "abcdefghij", "klmnopqrst")
valid_user3 = auth_register("3rd_email@valid.com", "123445678", "abcdefghij", "klmnopqrst")
print(valid_user)
print(valid_user2)
print(valid_user3)