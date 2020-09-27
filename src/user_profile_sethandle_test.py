'''
InputError when any of:
  handle_str must be between 3 and 20 characters
  handle is already used by another user

'''
from user import user_profile, user_profile_sethandle
from error import InputError
from other import clear
import pytest
import auth

def test_user_profile_sethandle():

    clear()

    # Register 2 users
    test_user_0 = auth.auth_register("test_email_0@email.com", "valid_pw0", "Hayden", "Jacobs")
    test_user_1 = auth.auth_register("test_email_1@email.com", "valid_pw1", "Jayden", "Haycobs")

    # Get test users' tokens
    test_user0_token = test_user_0['token']
    test_user1_token = test_user_1['token']

    # Get test users' u_id
    test_user0_id = test_user_0['u_id']
    test_user1_id = test_user_1['u_id']

    # Invalid handle string - str > 20 char in length
    with pytest.raises(InputError):
        user_profile_sethandle(test_user0_token, "A" * 21)

    # Invalid handle string - str < 3 char in length
    with pytest.raises(InputError):
        user_profile_sethandle(test_user0_token, "A")

    # Invalid handle string - handle already exists
    test_user1_profile = user_profile(test_user1_token, test_user1_id)
    with pytest.raises(InputError):
        user_profile_sethandle(test_user0_token, test_user1_profile['handle_str'])

    # Assert handle updates correctly
    user_profile_sethandle(test_user0_token, '1531_admin')
    test_user0_updated = user_profile(test_user0_token, test_user0_id)
    assert test_user0_updated['handle_str'] == "1531_admin"


