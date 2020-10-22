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

# check for correct name update
def test_profile_setname(url, initialisation):
    
    benjamin = initialisation
    query_string = urllib.parse.urlencode({
        'token' : benjamin['token'],
        'name_first': 'Ben',
        'name_last': 'Lon'
    })
    r = requests.get(f'{url}/user/profile/setname?{query_string}')
    update = r.json()

    # assert user_profile_setname(test_user0['token'], "Nick", "Smith") == {}

# check for invalid token
def test_profile_setname_invalid_token(url):

    r = requests.put(f'{url}/user/profile/setname?', json={
        'token' : 'invalid_token',
        'name_first': 'Ben',
        'name_last': 'Lon'
    })
    update = r.json()
    assert update['code'] == 400



# check for invalid first name input 
def test_profile_setname_fname_long(url, initialisation):    
    
    benjamin = initialisation
    
    # invalid firstname input - more than 50 characters
    query_string = urllib.parse.urlencode({
        'token' : benjamin['token'],
        'name_first': 'B' * 51,
        'name_last': 'Lon'
    })
    r = requests.get(f'{url}/user/profile/setname?{query_string}')
    update = r.json()
    assert update['code'] == 400
    

def test_profile_setname_fname_short(url, initialisation):
    
    benjamin = initialisation
    
    # Invalid first name input - input is space
    query_string = urllib.parse.urlencode({
        'token' : benjamin['token'],
        'name_first': ' ',
        'name_last': 'Lon',
    })
    r = requests.get(f'{url}/user/profile/setname?{query_string}')
    update = r.json()
    assert update['code'] == 400
    

# check for invalid last name input 
def test_profile_setname_invalid_lname_long(url, initialisation):        
    
    benjamin = initialisation
    
    # Invalid last name input - more than 50 characters
    query_string = urllib.parse.urlencode({
        'token' : benjamin['token'],
        'name_first': 'Bens',
        'name_last': 'L' * 51,
    })
    r = requests.get(f'{url}/user/profile/setname?{query_string}')
    update = r.json()
    assert update['code'] == 400

def test_profile_setname_invalid_lname_short(url, initialisation):    

    benjamin = initialisation
    
    # Invalid last name input - input is space
    query_string = urllib.parse.urlencode({
        'token' : benjamin['token'],
        'name_first': 'B',
        'name_last': ' '
    })
    r = requests.get(f'{url}/user/profile/setname?{query_string}')
    update = r.json()
    assert update['code'] == 400

