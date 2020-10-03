from error import InputError 
from other import clear
from auth import auth_register
import pytest

def test_auth_register1():

    clear()
    
    # When an email has a valid format but not registered yet
    # Register new user
    valid_user = auth_register("registered@valid.com", "potato321", "Elena", "Fisher")
    assert valid_user['u_id'] == 0

def test_valid_but_already_registered():
    
    # When the email has a valid format but is already registered
    with pytest.raises(InputError):
        auth_register("registered@valid.com", "potato321", "Elena", "Fisher")

def test_register_after_clear():

    clear()
    # When registered with same email after data is cleared
    valid_user = auth_register("registered@valid.com", "potato321", "Elena", "Fisher")
    assert valid_user['u_id'] == 0

def test_invalid_format_1():
    
    # When the email is of an invalid format 
    with pytest.raises(InputError):
        auth_register("email.com", "jamaica45678", "Elena", "Drake")

def test_invalid_format_2():
    
    #When email does not contain "".com" in the end
    with pytest.raises(InputError):
        auth_register("invalid@email", "fortunehunter", "Victor", "Sullivan")
    
def test_invalid_format_3():
    
    # when email contains 2 @s
    with pytest.raises(InputError):
        auth_register("two@@email.com", "narnia5566", "Nadine", "Ross")

def test_invalid_format_4():
    
    #When email doesn't contain "@example.com" type substring
    with pytest.raises(InputError):
        auth_register("eeeemail", "iamsotiredloool", "Nadine", "Ross")

def test_firstame_too_long():
    
    # When the first name is too long
    with pytest.raises(InputError):
        auth_register("sample@email.com", "harrypotter", "toomanychars"*20, "Vic")

def test_lastname_too_long():
    
    # When the last name is too long
    with pytest.raises(InputError):
        auth_register("sample@email.com", "okaygonnasleepnow", "toomanychars", "Vic"*30)

def test_password_too_short():
    # When the password is too short
    with pytest.raises(InputError):
        auth_register("sample@email.com", "smol", "Doom", "Slayer")