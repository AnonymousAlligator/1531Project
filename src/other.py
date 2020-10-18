from error import AccessError

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

#Returns a list of all users and their associated details
def users_all(token):
    check_token(token)

    users_list = []

    for user in data['users']:
        user_info = {
            'u_id' : user['u_id'],
            'email': user['email'], 
            'name_first':user['name_first'], 
            'name_last': user['name_last'], 
            'password': user['password'], 
            'handle': user['handle'],
            'token': user['token']
            }
        users_list.append(user_info)
    return users_list

def admin_userpermission_change(token, u_id, permission_id):
    pass

def search(token, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }

def check_token(token):

    # Searches for a logged in user through a token

    for user in data['users']:
        if user['token'] == token: # get() returns a value for the given key (token)
            return user

    # If the token doesn't exist/user isn't logged in
    raise AccessError("Token is not valid")

def find_with_uid(u_id):
    for user in data['users']:
        if u_id == user['u_id']:
            return(user)
    # If we are here then the token was invalid
    raise error.InputError('The user is not valid')