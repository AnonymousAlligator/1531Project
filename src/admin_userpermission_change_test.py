import pytest
import error
from auth import auth_register
from channels import channels_create
from test_helpers import create_one_test_user, create_two_test_users, create_three_test_users
from other import clear, admin_userpermission_change

def test_admin_userpermission_change_successtoowner():
    clear()
    user_0, user_1 = create_two_test_users()
    assert admin_userpermission_change(user_0['token'], user_1['u_id'], 1) == {}

def test_admin_userpermission_change_successtodefault():
    clear()
    user_0, user_1 = create_two_test_users()
    admin_userpermission_change(user_0['token'], user_1['u_id'], 1)
    assert admin_userpermission_change(user_0['token'], user_1['u_id'], 2) == {}


def test_admin_userpermission_change_invalidtoken():
    clear()
    user_0, user_1 = create_two_test_users()
    with pytest.raises(error.AccessError):
        assert admin_userpermission_change('hello', user_1['u_id'], 1) == {}

def test_admin_userpermission_change_notflockrowner():
    clear()
    user_0, user_1 = create_two_test_users()
    with pytest.raises(error.AccessError):
        assert admin_userpermission_change(user_1['token'], user_0['u_id'], 1) == {}

def test_admin_userpermission_change_userdoesnotexist():
    clear()
    user_0, user_1 = create_two_test_users()
    with pytest.raises(error.InputError):
        assert admin_userpermission_change(user_0['token'], 2, 1) == {}

def test_admin_userpermission_change_invalidpermissionid():
    clear()
    user_0, user_1 = create_two_test_users()
    with pytest.raises(error.InputError):
        assert admin_userpermission_change(user_0['token'], user_1['u_id'], 7) == {}