'''
InputError when any of:
Email entered is not a valid email using the method provided here (unless you feel you have a better method).
Email address is already being used by another user
'''
from user import user_profile, user_profile_setemail
from error import InputError
from other import clear
from test_helpers import create_one_test_user, create_two_test_users

import pytest
import re

# assert that email set works
def test_user_profile_setemail_works():
    clear()
    user_profile_setemail(test_user0_token, "cs1531@cse.unsw.edu.au")
    test_user0_updated = user_profile(test_user0_token, test_user0_id)
    assert test_user0_updated['email'] == "cs1531@cse.unsw.edu.au"

# check for invalid email - setting an existing user's email
def test_user_profile_setemail_existing():
    clear()	
    with pytest.raises(InputError):
        user_profile_setemail(test_user0_token, test_user1_profile['email'])

# check for invalid email address input - no '@' character		
def test_user_profile_setemail_invalid_check():
    clear()	
    with pytest.raises(InputError):
        user_profile_setemail(test_user0_token, 'asdsad.com')

# check for invalid email address input using email check helper function
def test_user_profile_setemail_invalid_check_helper():
    clear()	        
    assert emailCheck('test_email_0@email.com') == True
    assert emailCheck('invalid.com') == False		


# regex taken from https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
def emailCheck(email):  

        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        
        # pass the regular expression and the string in search() method 
        if(re.search(regex,email)):  
                return True  
                    
        return False
