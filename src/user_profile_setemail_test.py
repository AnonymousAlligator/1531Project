'''
InputError when any of:
Email entered is not a valid email using the method provided here (unless you feel you have a better method).
Email address is already being used by another user
'''
from user import user_profile, user_profile_setemail
from error import InputError
from other import clear, email_check
from test_helpers import create_one_test_user, create_two_test_users

import pytest

# assert that email set works
def test_user_profile_setemail_works():
    
    clear()
    test_user0 = create_one_test_user()

    user_profile_setemail(test_user0['token'], "test_email_9@email.com")
    test_user0_updated = user_profile(test_user0['token'], test_user0['u_id'])
    assert test_user0_updated['user']['email'] == "test_email_9@email.com"
    

# check for invalid email - setting an existing user's email
def test_user_profile_setemail_existing():
    
    clear()    
    test_user0, test_user1 = create_two_test_users()

    test_user1_profile = user_profile(test_user1['token'], test_user1['u_id'])

    with pytest.raises(InputError):
        user_profile_setemail(test_user0['token'], test_user1_profile['user']['email'])
    

# check for invalid email address input - no '@' character		
def test_user_profile_setemail_invalid_check():
    
    clear()
    test_user0 = create_one_test_user()

    with pytest.raises(InputError):
        user_profile_setemail(test_user0['token'], 'asdsad.com')


# check for invalid email address input using email check helper function
def test_user_profile_setemail_invalid_check_helper():

    assert email_check('bob@gmail.com') == True
    assert email_check('invalid.com') == False	    

