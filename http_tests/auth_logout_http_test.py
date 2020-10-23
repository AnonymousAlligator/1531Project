from url_fixture import url
import pytest
import requests

def test_auth_logout(url):

    requests.delete(f'{url}/clear')

    # Register users
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
    
    # When the token is valid 
    logout_return = requests.post(f'{url}/auth/logout', json={
        'token' : benjamin['token']
    })

    r = logout_return.json()
    assert r == {'is_success': True}
    
    logout_return2 = requests.post(f'{url}/auth/logout', json={
        'token' : ross['token']
    })

    r = logout_return2.json()
    assert r == {'is_success': True}
    
    logout_return3 = requests.post(f'{url}/auth/logout', json={
        'token' : benjamin['token']
    })

    r = logout_return3.json()
    assert r == {'is_success': False}

    logout_return4 = requests.post(f'{url}/auth/logout', json={
        'token' : ross['token']
    })

    r = logout_return4.json()
    assert r == {'is_success': False}

