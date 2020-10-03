from error import InputError 
from other import clear
from auth import auth_register, auth_logout, auth_login
import pytest

def test_auth_logout():

    clear()

    auth_dictionary0 = auth_register("validregistered@email.com", "1password", "Sam", "Drake")
    auth_dictionary1 = auth_register("validregistered1@email.com", "1password", "Sam", "Drake")
    
    # When the token is valid 
    assert auth_logout(auth_dictionary0['token']) == {'is_success': True}
    assert auth_logout(auth_dictionary1['token']) == {'is_success': True}
    
    #assert auth_logout(auth_dictionary0['token']) == {'is_success': False}
    #assert auth_logout(auth_dictionary1['token']) == {'is_success': False}
