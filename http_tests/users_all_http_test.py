from url_fixture import url
import pytest
import requests
import urllib

@pytest.fixture
def initialisation(url):

    # clear data
    requests.delete(f'{url}/clear')

    # register 2 users
    user0 = requests.post(f'{url}/auth/register', json={
        'email' : 'Benjamin@email.com',
        'password' : 'password',
        'name_first' : 'Benjamin',
        'name_last' : 'Long',
    })
    benjamin = user0.json()

    user1 = requests.post(f'{url}/auth/register', json={
        'email' : 'Ross@email.com',
        'password' : 'password',
        'name_first' : 'Ross',
        'name_last' : 'Short',
    })
    ross = user1.json()

    return benjamin, ross, 

# check attempt to list all 1 with a valid token
def test_http_users_all_1_valid_token(url, initialisation):

    benjamin = initialisation
    query_string = urllib.parse.urlencode({
        'token' : benjamin['token'],
    })
    r = requests.get(f'{url}/users/all?{query_string}')
    payload = r.json()
    assert payload['users'] == [{
        'users': [
            {
                "u_id" : 0,
                "email": "Benjamin@email.com",
                "name_first": "Benjamin",
                "name_last": "Long",
                "handle": "benjaminlong",
            },
        ]
    }]

# check attempt to list all 2 users with a valid token
def test_http_users_all_2_user1_valid_token(url, initialisation):
        
    benjamin = initialisation
    query_string = urllib.parse.urlencode({
        'token' : benjamin['token'],
    })
    r = requests.get(f'{url}/users/all?{query_string}')
    payload = r.json()
    
    assert payload['users'] == [{
        'users': [
            {
                "u_id" : 0,
                "email": "Benjamin@email.com",
                "name_first": "Benjamin",
                "name_last": "Long",
                "handle": "benjaminlong",
            },
            {
                "u_id" : 1,
                'email' : 'Ross@email.com',
                'name_first' : 'Ross',
                'name_last' : 'Short',
                'password' : 'rossshort',
            },
        ]
    }]
    
# check all 2 users return same list
def test_http_users_all_user2_valid_token(url, initialisation):

    _,ross  = initialisation
    query_string = urllib.parse.urlencode({
        'token' : ross['token'],
    })
    r = requests.get(f'{url}/users/all?{query_string}')
    payload = r.json()
    
    assert payload['users'] == [{
        'users': [
            {
                "u_id" : 0,
                "email": "Benjamin@email.com",
                "name_first": "Benjamin",
                "name_last": "Long",
                "handle": "benjaminlong",
            },
            {
                "u_id" : 1,
                'email' : 'Ross@email.com',
                'name_first' : 'Ross',
                'name_last' : 'Short',
                'password' : 'rossshort',
            },
        ]
    }]

# checks the order of list returned is in chronological u_id order
def test_http_users_all_valid_order(url, initialisation):

    benjamin = initialisation
    query_string = urllib.parse.urlencode({
        'token' : benjamin['token'],
    })
    r = requests.get(f'{url}/users/all?{query_string}')
    payload = r.json()

    assert payload['users'] != [{
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
    }]