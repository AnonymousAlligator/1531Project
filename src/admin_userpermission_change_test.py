import pytest
import error
from auth import auth_register
from channels import channels_create
from test_helpers import create_one_test_user, create_two_test_users, create_three_test_users
from other import clear, admin_userpermission_change

def test_admin_userpermission_change_success():
    clear()
    user_0, user_1 = create_two_test_users()
    assert admin_userpermission_change(user_0['token'], user_1['u_id'], 1) == {}