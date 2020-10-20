'''
InputError when any of:
  handle_str must be between 3 and 20 characters
  handle is already used by another user

'''
from user import user_profile, user_profile_sethandle
from error import InputError
from other import clear
from test_helpers import create_one_test_user, create_two_test_users
import pytest

# assert handle updates correctly
def test_user_profile_sethandle_works():

    clear()
    test_user_0 = create_one_test_user()
    # update the test_user0's handle
    assert user_profile_sethandle(test_user_0['token'], '1531_admin') == {}

# check for valid handle string - str = 20 char in length
def test_user_profile_sethandle_20():

    clear()
    test_user_0 = create_one_test_user()
    new_handle = "A" * 20
    assert user_profile_sethandle(test_user_0['token'], "A" * 20) == {}



# check for invalid handle string - str > 20 char in length
def test_user_profile_sethandle_short():

    clear()
    test_user_0 = create_one_test_user()

    with pytest.raises(InputError):
        user_profile_sethandle(test_user_0['token'], "A" * 21)


# check for invalid handle string - str < 3 char in length
def test_user_profile_sethandle_long():
    
    clear()
    test_user_0 = create_one_test_user()

    with pytest.raises(InputError):
        user_profile_sethandle(test_user_0['token'], "A")

 
# check for invalid handle string - handle already exists
def test_user_profile_sethandle_already_exists():
    
    clear()
    test_user_0, test_user_1 = create_two_test_users()

    with pytest.raises(InputError):
        user_profile_sethandle(test_user_0['token'], "jaydenhaycobs")
