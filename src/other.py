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
}



def clear():
    for value in data.values():
        del value[:]
    return {}

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
            'handle': user['handle'],
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
    messageslist = []
    #if query_str is empty
    if query_str.isspace():
        return {'messages': messageslist}
    #Check if token is correct
    caller = check_token(token)

    #loop through all channels and their messages and add message dictionary to the list
    for msg in data['messages']:
    #Check if the query_str is apart 
    #if TRUE for string inside string then append the message dictionary to list
        if query_str == msg['message'].lower():
            channelcheck = msg['channel_id']
            # Find the channel
            target_channel = {}
            for channel in data['channels']:
                if channelcheck == channel['channel_id']:
                    target_channel = channel
            # Input Error if the channel doesn't exist
            if target_channel == {}:
                #Input Error if the channel doesn't exist
                raise error.InputError('Channel does not exist')
                                
                for member in target_channel['all_members']:
                    if caller['u_id'] == member['u_id']:
                        messageslist.append(msg)

    return {'messages': messageslist}
    

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