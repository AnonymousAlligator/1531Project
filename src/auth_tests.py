import datetime 
import pytest 

def test_auth_login():

# Initial function calls before testing
    deactivate("registeredemail@valid.com")
    auth_dictionary = auth_register("registeredemail@valid.com", "password1", "Nathan", "Drake")
    user_token = auth_dictionary["token"]
    auth_logout(user_token)
    
# When the email is registered already with valid syntax
    auth_login("registeredemail@valid.com", "password1") == {"token" : user_token}
