from error import InputError 
from other import clear
from auth import auth_register, auth_logout, auth_login
import pytest

def test_auth_logout():

    clear()

    # deactivate("validregistered@email.com") @Taimoor - what does this function do?
    
    auth_dictionary = auth_register("validregistered@email.com", "1password", "Sam", "Drake")
    user_token = auth_dictionary["token"]
    invalid_token = "invalidtoken" # don't know if I need this

    # Token is invalid token
    assert auth_logout(invalid_token) == {'is_success': False} # don't know if I need this

    # When the token is valid 
    assert auth_logout(user_token) == {'is_success': True}

    #When token is already logged out
    assert auth_logout(user_token) == {'is_success': False}