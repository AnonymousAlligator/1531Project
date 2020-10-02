from error import InputError 
from other import clear
from auth import auth_register, auth_logout, auth_login
import pytest

def test_auth_logout():

    clear()

    # deactivate("validregistered@email.com") @Taimoor - what does this function do?
    
    auth_dictionary0 = auth_register("validregistered@email.com", "1password", "Sam", "Drake")
    
    
    # When the token is valid 
    assert auth_logout(auth_dictionary0['token']) == {'is_success': True}

    