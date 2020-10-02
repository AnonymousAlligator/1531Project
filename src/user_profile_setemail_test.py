'''
InputError when any of:
Email entered is not a valid email using the method provided here (unless you feel you have a better method).
Email address is already being used by another user
'''
from user import user_profile, user_profile_setemail
from error import InputError
from other import clear
import auth
import pytest
import re

# Register 2 test users
test_user_0 = auth.auth_register("test_email_0@email.com", "valid_pw0", "Hayden", "Jacobs")      
test_user_1 = auth.auth_register("test_email_1@email.com", "valid_pw1", "Jayden", "Haycobs")      

# Get test users' tokens
test_user0_token = test_user_0['token']	
test_user1_token = test_user_1['token']	

# Get test users' u_id
test_user0_id = test_user_0['u_id']
test_user1_id = test_user_1['u_id']

# Get test_user1's profile
test_user1_profile = user_profile(test_user1_token, test_user1_id)

# assert that email set works
def test_user_profile_setemail_works():
		
    user_profile_setemail(test_user0_token, "cs1531@cse.unsw.edu.au")
    test_user0_updated = user_profile(test_user0_token, test_user0_id)
    assert test_user0_updated['email'] == "cs1531@cse.unsw.edu.au"

# check for invalid email - setting an existing user's email
def test_user_profile_setemail_existing():
    
	with pytest.raises(InputError):
		user_profile_setemail(test_user0_token, test_user1_profile['email'])

# check for invalid email address input - no '@' character		
def test_user_profile_setemail_invalid_check():
    
    with pytest.raises(InputError):
        user_profile_setemail(test_user0_token, 'asdsad.com')

# check for invalid email address input using email check helper function
def test_user_profile_setemail_invalid_check_helper():
            
    assert emailCheck('test_email_0@email.com') == True
    assert emailCheck('invalid.com') == False		


# Modified email validity checker from https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
# as recommended in project spec
def emailCheck(email):  
	
		regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
		# pass the regular expression and the string in search() method 
		if(re.search(regex,email)):  
				return True  
					
		return False
				