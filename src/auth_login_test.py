from error import InputError 
from other import clear
from auth import auth_register, auth_logout, auth_login 
import pytest

def test_auth_login_and_register():
 
    clear()

    reg_dictionary = auth_register("registeredemail@valid.com", "password1", "Nathan", "Drake")
    reg_token = reg_dictionary['token']
    reg_uid = reg_dictionary['u_id']
    
    auth_logout(reg_token) #logout after registering
    
    login = auth_login("registeredemail@valid.com", "password1")
    login_token = login['token']
    login_uid = login['u_id']

    assert reg_uid == login_uid # check if u_id after login is same from when registering
    assert login_token == reg_token # check if token after login is same from when registering
# need to discuss

def test_auth_login_twice():

    clear()

    reg_dictionary2 = auth_register("registeredemail2@valid.com", "password1", "Nathan", "Drake")
    auth_logout(reg_dictionary2['token'])

    auth_login("registeredemail2@valid.com", "password1") #logged in for the first time

    # When the email is already logged in
    with pytest.raises(InputError):
        assert auth_login("registeredemail2@valid.com", "password1")
      

def test_auth_login_invalid_password():
    
    clear()

    reg_dictionary3 = auth_register("registeredemail3@valid.com", "password1", "Nathan", "Drake")
    auth_logout(reg_dictionary3['token'])

    # When the email is valid but password is not correct
    with pytest.raises(InputError):
        auth_login("registeredemail3@valid.com", "invalidpassword")
    
def test_auth_login_doesnt_exist():   
    
    clear()

    # When the email has valid syntax but is not registered (doesn't belong to a user)
    with pytest.raises(InputError):
        auth_login("unregisteredemail@valid.com", "3password3")

def test_auth_login_invalid_input():    

    clear()
    
    # When the input parameters are of invalid type or length
    with pytest.raises(InputError):
        auth_login(" ", "pword14602")
        auth_login("registered@email.com", "12345")
        auth_login("invalid.com", "a12345678")
