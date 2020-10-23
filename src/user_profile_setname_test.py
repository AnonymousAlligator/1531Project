'''
Update the authorised user's first and last name
InputError when any of:
name_first is not between 1 and 50 characters inclusively in length
name_last is not between 1 and 50 characters inclusively in length

'''
from user import user_profile_setname
from error import InputError, AccessError
from other import clear
from test_helpers import create_one_test_user
import pytest

# check for correct name update
def test_profile_setname():
    
    clear()    
    test_user0 = create_one_test_user()

    # TODO: update
    # assert user_profile_setname(test_user0['token'], "Nick", "Smith") == {}

# check for invalid token
def test_profile_setname_invalid_token():
    
    clear()
    create_one_test_user()

    with pytest.raises(AccessError):
        user_profile_setname('invalid_token', "Jayden", "Haycob")



# check for invalid first name input 
def test_profile_setname_fname_long():    
    
    clear()
    test_user0 = create_one_test_user()

    # Invalid firstname input - more than 50 characters
    with pytest.raises(InputError):
        user_profile_setname(test_user0['token'], "A" * 51, "valid_new_lname")

def test_profile_setname_fname_short():
    clear()
    test_user0 = create_one_test_user()
    
    # Invalid first name input - input is space
    with pytest.raises(InputError):
        user_profile_setname(test_user0['token'], " ", "valid_new_lname")
    

# check for invalid last name input 
def test_profile_setname_invalid_lname_long():        
    
    clear()
    test_user0 = create_one_test_user()

    # Invalid last name input - more than 50 characters
    with pytest.raises(InputError):
        user_profile_setname(test_user0['token'], "valid_new_fname", "A" * 51)

def test_profile_setname_invalid_lname_short():    
    clear()
    test_user0 = create_one_test_user()
    # Invalid last name input - input is space
    with pytest.raises(InputError):
        user_profile_setname(test_user0['token'], "valid_new_fname", " " )

