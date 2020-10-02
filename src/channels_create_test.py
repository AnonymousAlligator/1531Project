'''
InputError when channel name is more than 20 characters
'''


from channels import channels_create
from auth import auth_register
import error
import pytest
from test_helpers import create_one_test_user
from other import clear

channel_name1 = "Main Channel"
channel_name2 = "abcdefhijklmnopqrst"
channel_name3 = "abcdefhijklmnopqrstuvwxyz"


def test_channels_create_lessthan20():
    clear()
    test_user0 = create_one_test_user()
    # in assert, check for returned value
    assert channels_create(test_user0['token'], channel_name1, True) == 0


def test_channels_create_exactly20():
    clear()
    test_user0 = create_one_test_user()
    # in assert, check for returned value
    assert channels_create(test_user0['token'], channel_name2, True) == 0

def test_channels_create_morethan20():
    clear()
    test_user0 = create_one_test_user()

    with pytest.raises(error.InputError):
        channels_create(test_user0['token'], channel_name3, True)

def test_channels_create_public():
    # assert that public channel gets created - check channels_list_test
    pass

def test_channels_create_private():
    # assert that private channel gets created - check channels_list_test
    pass