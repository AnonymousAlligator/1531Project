'''
InputError when any of:
Email entered is not a valid email using the method provided here 
(unless you feel you have a better method).
Email address is already being used by another user
'''
from user import user_profile, user_profile_setemail
from error import InputError
from other import clear
from test_helpers import create_one_test_user, create_two_test_users

import pytest

# assert that email set works
def test_user_profile_setemail_works():
    
    clear()
    test_user0 = create_one_test_user()

    assert user_profile_setemail(test_user0['token'], "testemail9@email.com") == {}
    

# check for invalid email - setting an existing user's email
def test_user_profile_setemail_existing():
    
    clear()    
    test_user0, test_user1 = create_two_test_users()
    user_profile(test_user1["token"], ["u_id"])
    with pytest.raises(InputError):
        user_profile_setemail(test_user0['token'], "testemail1@email.com")
    

# check for invalid email address input - no '@' character		
def test_user_profile_setemail_invalid_check():
    
    clear()
    test_user0 = create_one_test_user()

    with pytest.raises(InputError):
        user_profile_setemail(test_user0['token'], 'asdsad.com')
