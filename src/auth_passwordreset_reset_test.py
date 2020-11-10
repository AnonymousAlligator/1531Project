from error import InputError 
from other import clear, data
from auth import auth_register, auth_passwordreset_reset, auth_logout
import pytest

def test_exception_auth_passwordreset_reset():

    clear()
    user_dict = auth_register("example@gmail.com", "password", "Nate", "Drake")
    
    user_token = user_dict["token"]
    auth_logout(user_token)

    with pytest.raises(InputError):
        auth_passwordreset_reset("99", "password")
