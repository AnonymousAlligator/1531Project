from error import InputError 
from other import clear
from auth import auth_register, auth_logout, auth_login
import pytest

def test_auth_logout():

    clear()

    # deactivate("validregistered@email.com") @Taimoor - what does this function do?
    
    auth_dictionary0 = auth_register("validregistered@email.com", "1password", "Sam", "Drake")
    auth_dictionary1 = auth_register("validregistered@email.com", "2password", "Drake", "Sam")
    user_token0 = auth_dictionary0["token"]
    user_token1 = auth_dictionary1["token"]
    
    invalid_token = "invalidtoken" # don't know if I need this

    # Token is invalid token
    assert auth_logout(invalid_token) == {'is_success': False} # don't know if I need this

    # When the token is valid 
    assert auth_logout(user_token0) == {'is_success': True}

    #When token is already logged out
    assert auth_logout(user_token1) == {'is_success': False}