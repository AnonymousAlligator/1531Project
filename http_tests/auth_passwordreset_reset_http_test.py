from url_fixture import url
import pytest
import requests

def test_exception_auth_passwordreset_reset(url):

    requests.delete(f'{url}/clear')

    # Register users
    user0 = requests.post(f'{url}/auth/register', json={
        'email' : 'Benjamin@email.com',
        'password' : 'password',
        'name_first' : 'Benjamin',
        'name_last' : 'Long',
    })

    benjamin = user0.json()

    requests.post(f'{url}/auth/logout', json={
        'token' : benjamin['token']
    })

    r = requests.post(f'{url}/auth/passwordreset/reset', json={
        'reset_code' : '99',
        "new_password" : "password"
    })

    payload = r.json()
    assert payload['code'] == 400
    