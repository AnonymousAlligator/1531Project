'''
InputError when any of user with u_id is not a valid user
For a valid user, returns information about their email, first name, last name, and handle
'''
from user import user_profile
from error import InputError
import auth
from other import clear
import pytest


def test_user_profile():
		
		clear()

		# Register 1 test user
		test_user_0 = auth.auth_register("cs1531@cse.unsw.edu.au", "valid_pw", "Hayden", "Jacobs")      
		test_user0_token = test_user_0['token']
		test_user0_id = test_user_0['u_id']

		# Invalid u_id with a valid token
		with pytest.raises(InputError):
				user_profile(test_user0_token, 100)

		# Invalid token with a valid u_id
		with pytest.raises(InputError):
				user_profile('invalid_token', 1)

		# Assert that a valid token and valid u_id returns the correct profile data
		assert(user_profile(test_user0_token, test_user0_id) == {
				'u_id': test_user0_id,
				'email': 'cs1531@cse.unsw.edu.au',
				'name_first': 'Hayden',
				'name_last': 'Jacobs',
				'handle_str': 'hjacobs',
				})

