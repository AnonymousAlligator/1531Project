from error import InputError 
from other import clear, data
from auth import auth_register
import pytest

def test_auth_register1():

    clear()
    
    # When an email has a valid format but not registered yet
    # Register new user
    valid_user = auth_register("registered@valid.com", "potato321", "Elena", "Fisher")
    assert valid_user['u_id'] == 0

    valid_user2 = auth_register("registered2@valid.com", "potato321", "Elena", "Fisher")
    assert valid_user2['u_id'] == 1
    

def test_valid_but_already_registered():

    clear()

    auth_register("registered@valid.com", "potato321", "Elena", "Fisher")
    auth_register("registered2@valid.com", "potato321", "Elena", "Fisher")

    # When the email has a valid format but is already registered
    with pytest.raises(InputError):
        auth_register("registered@valid.com", "potato321", "Poopy", "Poopface")
    # When the email has a valid format but is already registered
    with pytest.raises(InputError):
        auth_register("registered@valid.com", "potato321", "Elena", "Fisher")

def test_register_after_clear():

    clear()
    # When registered with same email after data is cleared
    valid_user = auth_register("registered@valid.com", "potato321", "Elena", "Fisher")
    assert valid_user['u_id'] == 0

def test_register_handle_length():

    clear()
    auth_register("registered@valid.com", "potato321", "Elena", "Fisher")
    auth_register("registered2@valid.com", "botato111", "Elena", "Fisher")
    handle_length_0 = len(data['users'][0]['handle_str'])
    handle_length_1 = len(data['users'][1]['handle_str'])

    assert handle_length_0 == 11
    assert data['users'][0]['handle_str'] == "elenafisher"
    
    assert handle_length_1 == 12
    assert data['users'][1]['handle_str'] == "elenafisher1"

    auth_register("registered3@valid.com", "botato111", "Elena"*3, "fivesss")
    
    handle_length_2 = len(data['users'][2]['handle_str'])
    
    assert handle_length_2 == 20
    assert data['users'][2]['handle_str'] == "elenaelenaelenafives"


def test_invalid_format_1():
    
    clear()
    # When the email is of an invalid format 
    with pytest.raises(InputError):
        auth_register("email.com", "jamaica45678", "Elena", "Drake")

def test_invalid_format_2():
    
    clear()
    # When email does not contain "".com" in the end
    with pytest.raises(InputError):
        auth_register("invalid@email", "fortunehunter", "Victor", "Sullivan")
    
def test_invalid_format_3():
    
    clear()
    # when email contains 2 @s
    with pytest.raises(InputError):
        auth_register("two@@email.com", "narnia5566", "Nadine", "Ross")

def test_invalid_format_4():
    
    clear()
    #When email doesn't contain "@example.com" type substring
    with pytest.raises(InputError):
        auth_register("eeeemail", "iamsotiredloool", "Nadine", "Ross")

def test_invalid_format_5():
    
    clear()
    #When email is empty
    with pytest.raises(InputError):
        auth_register(" ", "iamsotiredloool", "Nadine", "Ross")

def test_firstname_too_long():
    
    clear()
    # When the first name is too long
    with pytest.raises(InputError):
        auth_register("sample@email.com", "harrypotter", "toomanychars"*20, "Vic")

def test_firstname_too_short():
    
    clear()
    # When the first name is too short
    with pytest.raises(InputError):
        auth_register("sample@email.com", "harrypotter", "", "Vic")

def test_firstname_empty_space():
    
    clear()
    # When the first name is empty
    with pytest.raises(InputError):
        auth_register("sample@email.com", "harrypotter", "        ", "Vic")


def test_lastname_too_long():
    
    clear()
    # When the last name is too long
    with pytest.raises(InputError):
        auth_register("sample@email.com", "okaygonnasleepnow", "nottoomanychars", "boolean"*20)

def test_lastname_too_short():
    
    clear()
    # When the last name is too short
    with pytest.raises(InputError):
        auth_register("sample@email.com", "harrypotter", "nottoomanychars", "")


def test_lastname_empty_space():
    
    clear()
    # When thelast name is empty
    with pytest.raises(InputError):
        auth_register("sample@email.com", "harrypotter", "randomfirstname", "        ")


def test_password_too_short():
    
    clear()
    # When the password is too short
    with pytest.raises(InputError):
        auth_register("sample@email.com", "smol", "Doom", "Slayer")

        

