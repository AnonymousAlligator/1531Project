'''
Provide a list of all channels (and their associated details)
'''
from channels import channels_listall, channels_create
from auth import auth_register, auth_login
# from other import clear #TODO: uncomment once merged into all_tests

# register test users
test_user0 = auth_register("test_0@email.com", "0password0", "Hayden", "Jacobs") #returns { u_id, token }
test_user1 = auth_register("test_1@email.com", "1password1", "Jayden", "Haycobs") #returns { u_id, token }

test_user0_token = test_user0['token']
test_user0_token = test_user1['token']


# tests for listing one public channels
def test_channels_listall_public():
    # clear()
    
# tests for listing one private channels
def test_channels_listsall_private():
    # clear()

# tests for listing one of each public and private channels
def test_channels_listsall_both():
    # clear()

# tests for listing many of each public and private channels
def test_channels_listsall_many():
    # clear()
