import error

data = {
'users': [],
'channels': [
    #id: 'channel_id'
    #name: 'channel_name'
    #is_public: True or False
    #owner_members: [{u_id, name_first, name_last},]
    #all_members: [{u_id, name_first, name_last},]
    #messages:[{message_id, u_id, message, time_created},]
    ],
'messages': [
    #message_id: the message id
    #channel_id: the channel the message was sent to
    #u_id: user id of the person who sent the message
    #message: the message
    #time_created: when the message was created
    ],
'reset_data': {},    
}



def clear():
    
    data['users'] = []
    data['channels'] = []
    data['messages'] = []
    data['reset_data'] = {}
       

#Returns a list of all users and their associated details
def users_all(token):
    check_token(token)
    user_all_dict = {}
    users_list = []
    user_info = {}

    for user in data['users']:
        user_info = {
            'u_id' : user['u_id'],
            'email': user['email'],
            'name_first':user['name_first'],
            'name_last': user['name_last'],
            'handle_str': user['handle_str'],
            }
        users_list.append(user_info)
    user_all_dict ['users'] = users_list
    return user_all_dict

def admin_userpermission_change(token, u_id, permission_id):
    #Check if token is valid and record user
    caller = check_token(token)

    #Check if the caller of the function is an owner
    if caller['permission_id'] != 1:
        raise error.AccessError('You are not an owner of the flockr')

    #Check if user to be permission changed exists within database
    called = {}
    for user in data['users']:
        if u_id == user['u_id']:
            called = user
    # Input Error if the user doesn't exist
    if called == {}:
        raise error.InputError('User you are trying to change permissions for does not exist')

    #Check if permssion_id is a value permission, then change the permission_id of the user and add them to owner_list for channel
    if permission_id == 1:
        called['permission_id'] = 1
    elif permission_id == 2:
        called['permission_id'] = 2
    else:
        raise error.InputError('Incorrect value permission entered')

    return {}

def search(token, query_str):
    query_str.lower()
    messages_list = []
    channel_list = []
    #if query_str is empty
    if query_str.isspace():
        return {'messages': messages_list}
    #Check if token is correct
    caller = check_token(token)
    # Find all channels the caller is in
    for channel in data['channels']:
        for member in channel['all_members']:
            if caller['u_id'] == member['u_id']:
                channel_list.append(channel['id'])
    # go through dictionary of all messages and find messages that contain the query string
    for message in data['messages']:
        if query_str in message['message'].lower():
            # We found the message, now check if the user is part of the channel message was sent in
            if message['channel_id'] in channel_list:
                messages_list.append(message)
    return {'messages': messages_list}

def check_token(token):

    # Searches for a logged in user through a token
    for user in data['users']:
        if user['token'] == token: # get() returns a value for the given key (token)
            return user

    # If the token doesn't exist/user isn't logged in
    raise error.AccessError("Token is not valid")

#Finds user by u_ID, if the user does not exist then input error is given.
def find_with_uid(u_id):
    for user in data['users']:
        if u_id == user['u_id']:
            return(user)
    # If we are here then the token was invalid
    raise error.InputError('The user is not valid')
