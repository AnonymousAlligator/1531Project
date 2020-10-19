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
}



def clear():
    for value in data.values():
        del value[:]



def users_all(token):
    return {
        'users': [
            {
                'u_id': 1,
                'email': 'cs1531@cse.unsw.edu.au',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'hjacobs',
            },
        ],
    }

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

    #Check if permssion_id is a value permission
    if permission_id != 1 or permission_id != 2:
        raise error.InputError('Incorrect value permission entered')

    #Change the permission_id of the user and add them to owner_list for channel
    called['[permission_id'] == 1
    return {}

def search(token, query_str):
    messageslist = []
    if query_str.isspace():
        return messageslist
    #Check if token is correct
    for user in data['users']:
        if user['token'] == token:
            #loop through all channels and their messages and add message dictionary to the list
            for msg in data['channels']:
                #Check if the query_str is apart 
                for msgdata in msg['messages']:
                    #if TRUE for string inside string then append the message dictionary to list
                    if query_str in msgdata['message']:
                        messageslist.append(msg)
                return messageslist
    raise error.AccessError("Token is not valid")
    

def check_token(token):

    # Searches for a logged in user through a token

    for user in data['users']:
        if user['token'] == token: # get() returns a value for the given key (token)
            return user

    # If the token doesn't exist/user isn't logged in
    raise error.AccessError("Token is not valid")