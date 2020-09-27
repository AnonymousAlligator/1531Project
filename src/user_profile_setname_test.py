'''
Update the authorised user's first and last name
InputError when any of:
name_first is not between 1 and 50 characters inclusively in length
name_last is not between 1 and 50 characters inclusively in length

'''
from user import user_profile_setname
from error import InputError
import auth
import pytest

def user_profile_setname_test():
    
    # Register new user
    test_user_0 = auth.auth_register("valid_email@email.com", "valid_pw", "valid_fname", "valid_lname")  
    test_user0_token = test_user_0['token']

    # Invalid token
    with pytest.raises(InputError):
        user_profile_setname('invalid_token', "valid_newfname", "valid_newlname")
    
    # Invalid first name input - more than 50 characters
    with pytest.raises(InputError):
        user_profile_setname(test_user0_token, "A" * 51, "valid_new_lname")
    
    # Invalid first name input - input is 1 character
    with pytest.raises(InputError):
        user_profile_setname(test_user0_token, "A", "valid_new_lname")
    
    # Invalid last name input - more than 50 characters
    with pytest.raises(InputError):
        user_profile_setname(test_user0_token, "valid_new_fname", "A" * 51)
    
    # Invalid last name input - input is 1 character
    with pytest.raises(InputError):
        user_profile_setname(test_user0_token, "valid_new_fname", "A" )