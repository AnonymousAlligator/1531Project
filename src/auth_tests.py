import datetime 
import pytest 

def test_auth_login():

# Initial function calls before testing
    
    auth_dictionary = auth_register("registeredemail@valid.com", "password1", "Nathan", "Drake")
    user_token = auth_dictionary["token"]
    auth_logout(user_token) #logout after registering
    
    # When the email is registered already with valid syntax
    auth_login("registeredemail@valid.com", "password1") == {"token" : user_token}

    # When the email is already logged in
    with pytest.raises(InputError):
        auth_login("registeredemail@valid.com", "password1")
    auth_logout(user_token)

    # When the email is valid but password is not correct
    with pytest.raises(InputError):
        auth_login("registeredemail@valid.com", "invalidpassword1")
    

    # When the email has valid syntax but is not registered (doesn't belong to a user)
    with pytest.raises(InputError):
        auth_login("unregisteredemail@valid.com", "password3")
    
    # When the input parameters are of invalid type or length
    with pytest.raises(InputError):
        auth_login("", "pword14602")
        auth_login("registered@email.com", "12345")
        auth_login("invalid.com", "a12345678")
