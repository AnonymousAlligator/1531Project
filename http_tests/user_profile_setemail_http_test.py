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

# assert that email set works
def test_http_user_profile_setemail_works(url, initialisation):
    
    benjamin = initialisation
    # query_string = urllib.parse.urlencode({
    #     'token' : benjamin['token'],
    #     'email': 'benjamin2@email.com',
    # })

    # r = requests.put(f'{url}/user/profile/setemail?{query_string}')
    r = requests.put(f'{url}/user/profile/setemail?', json={
        'token' : benjamin['token'],
        'email': 'benjamin2@email.com',
    })
    payload = r.json()

    assert payload == {}
    

# check for invalid email - setting an existing user's email
def test_http_user_profile_setemail_existing(url, initialisation):
    
    benjamin = initialisation
    # query_string = urllib.parse.urlencode({
    #     'token' : benjamin['token'],
    #     'email': 'Ross@email.com',
    # })

    r = requests.put(f'{url}/user/profile/setemail?', json={
        'token' : benjamin['token'],
        'email': 'Ross@email.com',
    })
    payload = r.json()
    assert payload['code'] == 400
    

# check for invalid email address input - no '@' character		
def test_http_user_profile_setemail_invalid_check(url, initialisation):
    
    benjamin = initialisation
    query_string = urllib.parse.urlencode({
        'token' : benjamin['token'],
        'email': 'invalid_email.com',
    })

    r = requests.put(f'{url}/user/profile/setemail?{query_string}')
    payload = r.json()
    assert payload['code'] == 400
