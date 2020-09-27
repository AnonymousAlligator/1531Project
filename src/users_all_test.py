'''
Returns a list of all users and their associated details

'''
from other import users_all
import pytest
import auth

def users_all_test():
		
		#TODO: clear data

		# Register 3 test users
		test_user_0 = auth.auth_register("test_email_0@email.com", "valid_pw0", "Hayden", "Jacobs")      
		test_user_1 = auth.auth_register("test_email_1@email.com", "valid_pw1", "Jayden", "Haycobs")      
		test_user_2 = auth.auth_register("test_email_2@email.com", "valid_pw2", "Smith", "Smith")      
		
		# Get test users' tokens
		test_user0_token = test_user_0['token']	
		test_user1_token = test_user_1['token']	
		test_user2_token = test_user_2['token']	
		
		# attempt to list all users with a valid token
		assert len(users_all(test_user0_token)) == 3
		assert len(users_all(test_user1_token)) == 3
		assert len(users_all(test_user2_token)) == 3