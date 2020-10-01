'''
InputError when any of user with u_id is not a valid user
For a valid user, returns information about their email, first name, last name, and handle
'''
from user import user_profile
from error import InputError
from auth import auth_register
from other import clear
import pytest

# Register 1 users
test_user_0 = auth_register("test_email_0@email.com", "valid_pw0", "Hayden", "Jacobs")

# Get test user's tokens
test_user0_token = test_user_0['token']

# Get test user's u_id
test_user0_id = test_user_0['u_id']

# check that a valid token and valid u_id returns the correct profile data
def test_user_profile():		
		assert(user_profile(test_user0_token, test_user0_id) == {
				'u_id': test_user0_id,
				'email': 'cs1531@cse.unsw.edu.au',
				'name_first': 'Hayden',
				'name_last': 'Jacobs',
				'handle_str': 'hjacobs',
		})

# check for invalid token with a valid u_id
def test_user_profile_invalid_token():
		
		with pytest.raises(InputError):
				user_profile('invalid_token', test_user0_id)
		
		with pytest.raises(InputError):
				user_profile(12345678, test_user0_id)


# check for invalid u_id with a token
def test_user_profile_invalid_uid():

		with pytest.raises(InputError):
				user_profile(test_user0_token, 100)
		
		with pytest.raises(InputError):
				user_profile(test_user0_token, 2)

