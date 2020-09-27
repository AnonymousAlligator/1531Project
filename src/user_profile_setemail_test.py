'''
InputError when any of:
Email entered is not a valid email using the method provided here (unless you feel you have a better method).
Email address is already being used by another user
'''
from user import user_profile, user_profile_setemail
from error import InputError
import auth
import pytest

def user_profile_setemail_test():
  
    #TODO: clear data

	# Create test users
	test_user_0 = auth.auth_register("test_email_0@email.com", "valid_pw0", "Hayden", "Jacobs")      
	test_user_1 = auth.auth_register("test_email_1@email.com", "valid_pw1", "Jayden", "Haycobs")      
	
	# Get test users' tokens
	test_user0_token = test_user_0['token']	
	test_user1_token = test_user_1['token']	

	# Get test users' u_id
	test_user0_id = test_user_0['u_id']
	test_user1_id = test_user_1['u_id']
	
    # Invalid email address input - no '@' character
    #TODO: implement the suggestion below
	# https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/

    # Invalid email - existing user's email
	test_user1_profile = user_profile(test_user1_token, test_user1_id)
	with pytest.raises(InputError):
		user_profile_setemail(test_user0_token, test_user1_profile['email'])

	# Assert that email set works
	user_profile_setemail(test_user0_token, "cs1531@cse.unsw.edu.au")
	test_user0_updated = user_profile(test_user0_token, test_user0_id)
	assert test_user0_updated['email'] == "cs1531@cse.unsw.edu.au"
