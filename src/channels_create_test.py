'''
InputError when channel name is more than 20 characters
'''


from channels import channels_create
from auth import auth_register
import error
import pytest

Jeffo = auth_register("Jeffo@email.com", "a1b2c3", "Jeffo", "Jeff")

channel_name1 = "Main Channel"
channel_name2 = "abcdefhijklmnopqrst"
channel_name3 = "abcdefhijklmnopqrstuvwxyz"


def test_channels_create_lessthan20():
    assert channels_create(Dylan['token'], channel_name1, True) == 0


def test_channels_create_exactly20():
    assert channels_create(Dylan['token'], channel_name2, True) == 0

def test_channels_create_morethan20():
    with pytest.raises(error.InputError):
        assert channels_create(Dylan['token'], channel_name3, True)

#assume that name given is a string
