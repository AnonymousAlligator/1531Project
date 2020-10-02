from error import InputError 
from other import clear
from auth import auth_register, auth_logout, auth_login 
import pytest

def test_auth_login():

# Initial function calls before testing
    
    clear()

    reg_dictionary = auth_register("registeredemail@valid.com", "password1", "Nathan", "Drake")
    reg_token = reg_dictionary['token']
    reg_uid = reg_dictionary['u_id']
    
    auth_logout(reg_token) #logout after registering
    
    login = auth_login("registeredemail@valid.com", "password1")
    login_token = login['token']
    login_uid = login['u_id']

    assert reg_uid == login_uid
    assert auth_logout(login_token) == {'is_success': True}
    #assert auth_logout(login_token) == {'is_success': False}

    # When the email is already logged in
    #with pytest.raises(InputError):
    #    auth_login("registeredemail@valid.com", "password1")
        # auth_logout(user_token) #TODO @Taimoor - error as user_token isn't defined

    # When the email is valid but password is not correct
    with pytest.raises(InputError):
        auth_login("registeredemail@valid.com", "invalidpassword1")
    
    # When the email has valid syntax but is not registered (doesn't belong to a user)
    #with pytest.raises(InputError):
    #    auth_login("unregisteredemail@valid.com", "3password3")
    
    # When the input parameters are of invalid type or length
    with pytest.raises(InputError):
        auth_login("", "pword14602")
        auth_login("registered@email.com", "12345")
        auth_login("invalid.com", "a12345678")
