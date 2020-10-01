'''
Provide a list of all channels (and their associated details) that the authorised user is part of
'''
from channels import channels_listall
from auth_register import auth_register
from auth_login import auth_login
from channels_create import channels_create
from other import clear

# create users for testing
user_0 = auth_register("test_0@email.com", "0password0", "Hayden", "Jacobs") #returns { u_id, token }
user_1 = auth_register("test_1@email.com", "1password1", "Jayden", "Haycobs") #returns { u_id, token }



# tests for listing one public channels
def test_channels_listall_public():
    clear()

    

# tests for listing one private channels
def test_channels_listsall_private():
    clear()

# tests for listing one of each public and private channels
def test_channels_listsall_both():
    clear()

# tests for listing many of each public and private channels
def test_channels_listsall_both():
    clear()

"""
def channels_listall(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }
"""