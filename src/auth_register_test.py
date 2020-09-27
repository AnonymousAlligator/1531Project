from error import InputError 
from other import clear
from auth import auth_register
import pytest

def test_auth_register():

    clear()
    
    # When an email has a valid format but not registered yet
    # Register new user
    valid_user = auth_register("registered@valid.com", "potato321", "Elena", "Fisher")
    assert valid_user['u_id'] == 1

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

    # When the last name is too long
    with pytest.raises(InputError):
        auth_register("sample@email.com", "okaygonnasleepnow", "toomanychars", "Vic"*30)

    # When the password isn't valid
    with pytest.raises(InputError):
        auth_register("sample@email.com", "smol", "Doom", "Slayer")