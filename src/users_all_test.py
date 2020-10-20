'''
Returns a list of all users and their associated details

'''
from other import users_all
import pytest
from other import clear
from test_helpers import create_one_test_user, create_two_test_users, create_three_test_users

# check attempt to list all 1 with a valid token
def test_users_all_1_valid_token():

    clear()
    user0 = create_one_test_user()

    assert(users_all(user0['token']) == {
        'users': [
            {
                "u_id" : 0,
                "email": "testemail0@email.com",
                "name_first": "Hayden",
                "name_last": "Jacobs",
                "handle": "haydenjacobs",
            },
        ]
    })

# check attempt to list all 2 users with a valid token
def test_users_all_2_user1_valid_token():
        
    clear()
    user0, user1 = create_two_test_users()
    assert(users_all(user0['token']) == {
        'users': [
            {
                "u_id" : 0,
                "email": "testemail0@email.com",
                "name_first": "Hayden",
                "name_last": "Jacobs",
                "handle": "haydenjacobs",
            },
            {
                "u_id" : 1,
                "email": "testemail1@email.com",
                "name_first": "Jayden",
                "name_last": "Haycobs",
                "handle": "jaydenhaycobs",
            },
        ]
    })
    
    # check all 2 users return same list

def test_users_all_user2_valid_token():

    clear()
    user0, user1 = create_two_test_users()

    assert(users_all(user1['token']) == {
        'users': [
            {
                "u_id" : 0,
                "email": "testemail0@email.com",
                "name_first": "Hayden",
                "name_last": "Jacobs",
                "handle": "haydenjacobs",
            },            
            {
                "u_id" : 1,
                "email": "testemail1@email.com",
                "name_first": "Jayden",
                "name_last": "Haycobs",
                "handle": "jaydenhaycobs",
            },

        ]
    })

# checks the order of list returned is in chronological u_id order
def test_users_all_valid_order():

    clear()
    user0, user1 = create_two_test_users()

    assert(users_all(user1['token']) != {
        'users': [
            {
                "u_id" : 1,
                "email": "testemail1@email.com",
                "name_first": "Jayden",
                "name_last": "Haycobs",
                "handle": "jaydenhaycobs",
            },
            {
                "u_id" : 0,
                "email": "testemail0@email.com",
                "name_first": "Hayden",
                "name_last": "Jacobs",
                "handle": "haydenjacobs",
            },
        ]
    })