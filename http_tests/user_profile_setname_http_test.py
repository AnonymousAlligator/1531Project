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

    return benjamin

# check for correct name payload
def test_http_profile_setname(url, initialisation):
    
    benjamin = initialisation

    r = requests.put(f'{url}/user/profile/setname',json={
        'token' : benjamin['token'],
        'name_first': 'Ben',
        'name_last': 'Lon'
    })
    payload = r.json()

    assert payload == {}

# check for invalid token
def test_http_profile_setname_invalid_token(url):

    r = requests.put(f'{url}/user/profile/setname?', json={
        'token' : 'invalid_token',
        'name_first': 'Ben',
        'name_last': 'Lon'
    })
    payload = r.json()
    assert payload['code'] == 400



# check for invalid first name input 
def test_http_profile_setname_fname_long(url, initialisation):    
    
    benjamin = initialisation
    
    # invalid firstname input - more than 50 characters
    r = requests.put(f'{url}/user/profile/setname',json={
        'token' : benjamin['token'],
        'name_first': 'B' * 51,
        'name_last': 'Lon'
    }) 
    payload = r.json()
    assert payload['code'] == 400
    

def test_http_profile_setname_fname_short(url, initialisation):
    
    benjamin = initialisation
    
    # Invalid first name input - input is space
    r = requests.put(f'{url}/user/profile/setname',json={
        'token' : benjamin['token'],
        'name_first': ' ',
        'name_last': 'Lon',
    }) 
    payload = r.json()
    assert payload['code'] == 400
    

# check for invalid last name input 
def test_http_profile_setname_invalid_lname_long(url, initialisation):        
    
    benjamin = initialisation
    
    # Invalid last name input - more than 50 characters
    r = requests.put(f'{url}/user/profile/setname',json={
        'token' : benjamin['token'],
        'name_first': 'Bens',
        'name_last': 'L' * 51,
    }) 
    payload = r.json()
    assert payload['code'] == 400

def test_http_profile_setname_invalid_lname_short(url, initialisation):    

    benjamin = initialisation
    
    # Invalid last name input - input is space
    r = requests.put(f'{url}/user/profile/setname',json={
        'token' : benjamin['token'],
        'name_first': 'B',
        'name_last': ' '
    }) 
    payload = r.json()
    assert payload['code'] == 400

