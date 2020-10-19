'''
Returns a list of all users and their associated details

'''
from other import users_all
import pytest
from other import clear
from test_helpers import create_one_test_user, create_two_test_users, create_three_test_users

# check attempt to list all 1 with a valid token
def test_users_all_1_valid_token():
				
		clear()
		user0 = create_one_test_user()
		
		# check all 1 user return same list
		assert len(users_all(user0['token'])) == 1

# check attempt to list all 2 users with a valid token
def test_users_all_2_valid_token():
		
		clear()
		user0, user1 = create_two_test_users()
		
		# check all 2 users return same list
		assert len(users_all(user0['token'])) == 2
		assert len(users_all(user1['token'])) == 2

# check attempt to list all 3 users with a valid token
def test_users_all_3_valid_token():
		
		clear()
		user0, user1, user2 = create_three_test_users()
		
		# check all 3 users return same list
		assert len(users_all(user0['token'])) == 3
		assert len(users_all(user1['token'])) == 3
		assert len(users_all(user2['token'])) == 3