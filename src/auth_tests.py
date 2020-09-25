import datetime 
import pytest 

def test_auth_login():

# Initial function calls before testing
    
    reg_dictionary = auth_register("registeredemail@valid.com", "password1", "Nathan", "Drake")
    reg_token = reg_dictionary['token']
    reg_uid = reg_dictionary['u_id']
    
    auth_logout(reg_token) #logout after registering
    
    login = auth_login("registeredemail@valid.com", "password1")
    login_token = login['token']
    login_uid = login['u_id']

    assert reg_uid == login_uid
    assert auth_logout(login_token) == {'is_success': True}
    assert auth_logout(login_token) == {'is_success': False}

    # When the email is already logged in
    with pytest.raises(InputError):
        auth_login("registeredemail@valid.com", "password1")
    auth_logout(user_token)

    # When the email is valid but password is not correct
    with pytest.raises(InputError):
        auth_login("registeredemail@valid.com", "invalidpassword1")
    
    # When the email has valid syntax but is not registered (doesn't belong to a user)
    with pytest.raises(InputError):
        auth_login("unregisteredemail@valid.com", "3password3")
    
    # When the input parameters are of invalid type or length
    with pytest.raises(InputError):
        auth_login("", "pword14602")
        auth_login("registered@email.com", "12345")
        auth_login("invalid.com", "a12345678")

########################################################

def test_auth_logout():

    deactivate("validregistered@email.com")
    auth_dictionary = auth_register("validregistered@email.com", "1password", "Sam", "Drake")
    user_token = auth_dictionary["token"]
    invalid_token = "invalidtoken" # don't know if I need this

    # Token is invalid token
    assert auth_logout(invalid_token) == {'is_success': False} # don't know if I need this

    # When the token is valid 
    assert auth_logout(user_token) == {'is_success': True}

    #When token is already logged out
    assert auth_logout(user_token) == {'is_success': False}

########################################################

def test_auth_register():

    # When an email has a valid format but not registered yet
    auth_register("registered@valid.com", "potato321", "Elena", "Fisher")

    # When the email has a valid format but is already registered
    with pytest.raises(InputError):
        auth_register("registered@valid.com", "potato321", "Elena", "Fisher")

    # When the email is of an invalid format 
    with pytest.raises(InputError):
        auth_register("email.com", "jamaica45678", "Elena", "Drake")

    with pytest.raises(InputError):
        auth_register("invalid@email", "fortunehunter", "Victor", "Sullivan")
    
    with pytest.raises(InputError):
        auth_register("two@@email.com", "narnia5566", "Nadine", "Ross")

    with pytest.raises(InputError):
        auth_register("eeeemail", "iamsotiredloool", "Nadine", "Ross")

    # When the first name is too long
    with pytest.raises(InputError):
        auth_register("sample@email.com", "harrypotter", "toomanychars"*20, "Vic")

    # When the first name is too long
    with pytest.raises(InputError):
        auth_register("sample@email.com", "okaygonnasleepnow", "toomanychars", "Vic"*30)

    # When the password isn't valid
    with pytest.raises(InputError):
        auth_register("sample@email.com", "smol", "Doom", "Slayer")
    



