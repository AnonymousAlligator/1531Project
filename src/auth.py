import re 

def auth_login(email, password):
    
    for user in data['users']:
        if user['email'] == email:
            found_user = user

    if not found_user:
        raise InputError('Email has not been registered previously')
    
    if password != found_user['password']:
        raise InputError('Password entered is not correct')
    
    token = email # not sure what else to do with token here
    
    return {
        'u_id': found_user[u_id], 'token': token,
    }

def auth_logout(token):
    
    data = DATABASE

    user = check_token(token)
    
    flag = False
       
    if user['token'][token]:
        for info in data[users]:
            if info == user:
                info['token'][token] = flag    # # Invalidates the user token
                break
        flag = True

    return {'is_success': flag}

def auth_register(email, password, name_first, name_last):
    
    # Password needs to be at least 6 characters long
    if len(password) < 6:
        raise InputError('Password entered is less than 6 characters long')


    email_match = r'^\w+([\.-]?\w+)*@\w([\.-]?\w+)*(\.\w{2,3})+$'
    if not re.search(email_match, email): # If it returns FALSE
        raise InputError('Entered email is not valid')

    first_name_length= len(name_first)
    last_name_length= len(name_last)

    # First name doesn't contain at least 1 character
    if len(name_first) < 1:
        raise InputError('First name is less than 1 character long')

    # First name contains more than 50 characters
    if len(name_first) > 50:
        raise InputError('First name is more than 50 characters long')

    if len(name_last) < 1:
        raise InputError('Last name is less than 1 character long')

    if len(name_last) > 50: 
        raise InputError('Last name is more than 50 characters long')

    # Check if email already registered
    for registered_user in data['users']:
        if registered_user['email'] == email:
            raise InputError('Email already taken by another registered user')

    u_id = len(data['users']) # checks the number of people in the users database to establish the u_id

    #pID = 2 # member ID by default
    #if u_id == 0:
    #    pID = 1 # first user in the server so changed to owner       

    data['users'].append({
        'u_id': u_id, 
        #'p_id': pID, 
        'email': email, 
        'name_first':name_first, 
        'name_last': name_last, 
        'password': password, 
        'handle': handle, 
        'token': email,
    })

    return {
        'u_id': u_id,
        'token': email,
    }

def check_token(token):

    # Searches for a logged in user through a token

    data = DATABASE
    for user in data['users']:
        if user['token'].get(token, None): # get() returns a value for the given key (token)
            return user

    # If the token doesn't exist/user isn't logged in
    raise AccessError("Token is not valid")
