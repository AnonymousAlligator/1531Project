'''
InputError when any of user with u_id is not a valid user
For a valid user, returns information about their email, first name, last name, and handle_str
'''
from user import user_profile
import error
from other import clear
from test_helpers import create_one_test_user
import pytest


# check that a valid token and valid u_id returns the correct profile data
def test_user_profile():	
    
    clear()	
    test_user0 = create_one_test_user()
    
    assert user_profile(test_user0['token'], test_user0['u_id']) == {
        'user':
            {
            'u_id': test_user0['u_id'], 
            'email': 'testemail0@email.com', 
            'name_first': 'Hayden', 
            'name_last': 'Jacobs', 
            'handle_str': 'haydenjacobs',
            'profile_img_url': '',
            }
    }

# check for invalid token with a valid u_id
def test_user_profile_invalid_token():
    
    clear()	
    test_user0 = create_one_test_user()

    with pytest.raises(error.AccessError):
        user_profile('invalid_token', test_user0['u_id'])

# check for invalid u_id with a token
def test_user_profile_invalid_uid():
    
    clear()	    
    test_user0 = create_one_test_user()

    with pytest.raises(error.InputError):
        user_profile(test_user0['token'], 100)

