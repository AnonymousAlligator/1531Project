from url_fixture import url
import pytest
import requests

@pytest.fixture
def initialisation(url):
    #clear data
    requests.delete(f'{url}/clear')
    #register test users
    user1 = requests.post(f'{url}/auth/register', json={
        'email' : 'Ross@email.com',
        'password' : 'password',
        'name_first' : 'Ross',
        'name_last' : 'Short',
    })
    ross = user1.json()
    return ross

def test_user_profile_photo_success(url, initialisation):
    user0 = initialisation
    r = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token' : user0['token'],
    })
    payload = r.json()
    
    assert payload == {}