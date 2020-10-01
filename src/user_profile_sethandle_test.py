'''
InputError when any of:
  handle_str must be between 3 and 20 characters
  handle is already used by another user

'''
from user import user_profile, user_profile_sethandle
from auth import auth_register
from error import InputError
from other import clear
import pytest

# Register 2 users
test_user_0 = auth_register("test_email_0@email.com", "valid_pw0", "Hayden", "Jacobs")
test_user_1 = auth_register("test_email_1@email.com", "valid_pw1", "Jayden", "Haycobs")

# Get test users' tokens
test_user0_token = test_user_0['token']
test_user1_token = test_user_1['token']

# Get test users' u_id
test_user0_id = test_user_0['u_id']
test_user1_id = test_user_1['u_id']

# assert handle updates correctly
def test_user_profile_sethandle_works():    
    
    # update the test_user0's handle
    user_profile_sethandle(test_user0_token, '1531_admin')    
    # get test_user0's profile
    test_user0_updated = user_profile(test_user0_token, test_user0_id)

    assert test_user0_updated['handle_str'] == "1531_admin"

# check for invalid handle string - str > 20 char in length
def test_user_profile_sethandle_short():
    with pytest.raises(InputError):
        user_profile_sethandle(test_user0_token, "A" * 21)

    with pytest.raises(InputError):
        user_profile_sethandle(test_user0_token, "A" * 200)

# check for invalid handle string - str < 3 char in length
def test_user_profile_sethandle_long():
    with pytest.raises(InputError):
        user_profile_sethandle(test_user0_token, "A")    

    with pytest.raises(InputError):
        user_profile_sethandle(test_user0_token, "aa")    

# check for invalid handle string - handle already exists
def test_user_profile_sethandle_exists():

    # get test_user1's profile
    test_user1_profile = user_profile(test_user1_token, test_user1_id)

    with pytest.raises(InputError):
        user_profile_sethandle(test_user0_token, test_user1_profile['handle_str'])


