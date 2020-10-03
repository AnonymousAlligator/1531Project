'''
Update the authorised user's first and last name
InputError when any of:
name_first is not between 1 and 50 characters inclusively in length
name_last is not between 1 and 50 characters inclusively in length

'''
from user import user_profile_setname, user_profile
from error import InputError
from other import clear
from test_helpers import create_one_test_user
import pytest


# check for correct name update
def test_profile_setname():
    
    clear()    

    # TODO: update in iter2
    # test_user0 = create_one_test_user()

    # user_profile_setname(test_user0['token'], "Nick", "Smith")    
    # updated_test_user_0 = user_profile(test_user0['token'], test_user_0['u_id'])    
    # assert updated_test_user_0['name_first'] == "Nick"
    # assert updated_test_user_0['name_last'] == "Smith"

    pass

# check for invalid token
def test_profile_setname_invalid_token():
    
    clear()
    # create_one_test_user()

    # with pytest.raises(InputError):
    #     user_profile_setname('invalid_token', "Jayden", "Haycob")

    # with pytest.raises(InputError):
    #     user_profile_setname(123456, "Jayden", "Haycob")

    pass

# check for invalid first name input 
def test_profile_setname_invalid_fname():    
    
    clear()
    # test_user0 = create_one_test_user()

    # # Invalid firstname input - more than 50 characters
    # with pytest.raises(InputError):
    #     user_profile_setname(test_user0['token'], "A" * 51, "valid_new_lname")
    
    # with pytest.raises(InputError):
    #     user_profile_setname(test_user0['token'], "A" * 100, "valid_new_lname")
    
    # # Invalid first name input - input is 1 character
    # with pytest.raises(InputError):
    #     user_profile_setname(test_user0['token'], "A", "valid_new_lname")
    
    pass

# check for invalid last name input 
def test_profile_setname_invalid_lname():        
    
    clear()
    # test_user0 = create_one_test_user()

    # # Invalid last name input - more than 50 characters
    # with pytest.raises(InputError):
    #     user_profile_setname(test_user0['token'], "valid_new_fname", "A" * 51)
    
    # with pytest.raises(InputError):
    #     user_profile_setname(test_user0['token'], "valid_new_fname", "A" * 100)
    
    # # Invalid last name input - input is 1 character
    # with pytest.raises(InputError):
    #     user_profile_setname(test_user0['token'], "valid_new_fname", "A" )
    pass
