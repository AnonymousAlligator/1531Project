from error import InputError 
from other import clear, data, clearer
from auth import auth_register, auth_passwordreset_reset, auth_logout
import pytest

def test_exception_passwordreset_reset():

    """ Tests exceptions for password_reset """

    # Set up before testing
    clearer()
    user_dict = auth_register("example@gmail.com", "password", "Nate", "Drake")
    
    user_token = user_dict["token"]
    auth_logout(user_token)

    # only thing we can test through pytest is invalid reset code
    with pytest.raises(InputError):
        auth_passwordreset_reset("99", "password")