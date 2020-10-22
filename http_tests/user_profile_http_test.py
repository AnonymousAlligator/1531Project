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

# check that a valid token and valid u_id returns the correct profile data
def test_user_profile(url, initialisation):	
    
    benjamin = initialisation
    query_string = urllib.parse.urlencode({
        'token' : benjamin['token'],
        'u_id' : benjamin['u_id'],        
    })
    r = requests.get(f'{url}/channel/details?{query_string}')
    profile = r.json()

    assert(profile(benjamin['token'], benjamin['u_id']) == {
        'user': [
            {
            'u_id': benjamin['u_id'], 
            'email': 'Benjamin@email.com', 
            'name_first': 'Benjamin', 
            'name_last': 'Long', 
            'handle': 'benjaminlong',
            },
        ]
    })

# check for invalid token with a valid u_id
def test_user_profile_invalid_token(url, initialisation):
    
    clear()	
    test_user0 = create_one_test_user()

    with pytest.raises(error.AccessError):
        user_profile('invalid_token', test_user0['u_id'])

# check for invalid u_id with a token
def test_user_profile_invalid_uid(url, initialisation):
    
    clear()	    
    test_user0 = create_one_test_user()

    with pytest.raises(error.InputError):
        user_profile(test_user0['token'], 100)

