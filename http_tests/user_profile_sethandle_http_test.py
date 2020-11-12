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

# assert handle updates correctly
def test_http_user_profile_sethandle_works(url, initialisation):

    benjamin,_ = initialisation
    r = requests.put(f'{url}/user/profile/sethandle', json={
        'token' : benjamin['token'],
        'handle_str': 'blong',
    })
    payload = r.json()

    assert payload == {}

# assert handle updates correctly
def test_http_user_profile_sethandle_strip(url, initialisation):

    benjamin,_ = initialisation
    r = requests.put(f'{url}/user/profile/sethandle', json={
        'token' : benjamin['token'],
        'handle_str': 'blong   ',
    })
    payload = r.json()

    assert payload == {}

# check for valid handle string - str = 20 char in length
def test_http_user_profile_sethandle_20(url, initialisation):    

    benjamin,_ = initialisation
    r = requests.put(f'{url}/user/profile/sethandle', json={
        'token' : benjamin['token'],
        'handle_str': 'b' * 20,
    })
    payload = r.json()

    assert payload == {}

# check for invalid handle string - str > 20 char in length
def test_http_user_profile_sethandle_long(url, initialisation):

    benjamin,_ = initialisation

    r = requests.put(f'{url}/user/profile/sethandle', json={
        'token' : benjamin['token'],
        'handle_str': 'b' * 21,
    })
    payload = r.json()
    assert payload['code'] == 400

# check for invalid handle string - str < 3 char in length
def test_http_user_profile_sethandle_short(url, initialisation):
    
    benjamin,_ = initialisation

    r = requests.put(f'{url}/user/profile/sethandle', json={
        'token' : benjamin['token'],
        'handle_str': 'BL',
    })
    payload = r.json()
    assert payload['code'] == 400

 
# check for invalid handle string - handle already exists
def test_http_user_profile_sethandle_already_exists(url, initialisation):
    
    benjamin,_ = initialisation

    r = requests.put(f'{url}/user/profile/sethandle', json={
        'token' : benjamin['token'],
        'handle_str': 'rossshort',
    })
    payload = r.json()
    assert payload['code'] == 400

# token invalid
def test_http_user_profile_sethandle_invalid_token(url, initialisation):

    _,_ = initialisation
    r = requests.put(f'{url}/user/profile/sethandle', json={
        'token' : 'boop',
        'handle_str': 'blong',
    })
    payload = r.json()

    assert payload['code'] == 400
