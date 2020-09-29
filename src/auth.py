import re 

def auth_login(email, password):
    
    for user in backend_database['users']:
        if user['email'] == email:
            found_user = user

    if not found_user:
        raise InputError('Email has not been registered previously')
    
    if password != found_user['password']:
        raise InputError('Password entered is not correct')
    
    return {
        'u_id': int(found_user[uID], 'token': token,
    }

def auth_logout(token):
    return {
        'is_success': True,
    }

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
    for registered_user in backend_database['users']:
        if registered_user['email'] == email:
            raise InputError('Email already taken by another registered user')

    uID = len(backend_database['users']) # checks the number of people in the users database to establish the uID

    pID = 2 # member ID by default
    if uID == 0:
        pID = 1 # first user in the server so changed to owner       

    backend_database['users'].append({
        'u_id': str(uID), 'p_id': pID, 'email': email, 'name_first':name_first, 'name_last': name_last, 'password': password, 'handle': handle, 'token': email,
    })

    return {
        'u_id': uID,
        'token': email,
    }
