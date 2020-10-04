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

@pytest.mark.skip(reason='function implementation not done yet')
# assert handle updates correctly
def test_user_profile_sethandle_works():

    clear()
    test_user0 = create_one_test_user()

    # update the test_user0's handle
    user_profile_sethandle(test_user0['token'], '1531_admin')
    # get test_user0's profile
    test_user0_updated = user_profile(test_user0['token'], test_user0['u_id'])

    assert test_user0_updated['handle_str'] == "1531_admin"

@pytest.mark.skip(reason='function implementation not done yet')
# check for invalid handle string - str > 20 char in length
def test_user_profile_sethandle_short():

    clear()
    test_user0, test_user1 = create_two_test_users()

    with pytest.raises(InputError):
        user_profile_sethandle(test_user0['token'], "A" * 21)

    with pytest.raises(InputError):
        user_profile_sethandle(test_user1['token'], "A" * 200)
    
@pytest.mark.skip(reason='function implementation not done yet')
# check for invalid handle string - str < 3 char in length
def test_user_profile_sethandle_long():
    
    clear()
    test_user0, test_user1 = create_two_test_users()

    with pytest.raises(InputError):
        user_profile_sethandle(test_user0['token'], "A")

    with pytest.raises(InputError):
        user_profile_sethandle(test_user1['token'], "aa")

@pytest.mark.skip(reason='function implementation not done yet')    
# check for invalid handle string - handle already exists
def test_user_profile_sethandle_exists():
    
    clear()
    test_user0, test_user1 = create_two_test_users()
    
    # get test_user1's profile
    test_user1_profile = user_profile(test_user1['u_id'], test_user1['u_id'])

    with pytest.raises(InputError):
        user_profile_sethandle(test_user0['token'], test_user1_profile['handle_str'])
    

