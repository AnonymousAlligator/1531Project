from url_fixture import url
import pytest
import requests

def test_auth_login_and_register(url):
     
    # Clear data space
    requests.delete(f'{url}/clear')

    # Register users
    user0 = requests.post(f'{url}/auth/register', json={
        'email' : 'Benjamin@email.com',
        'password' : 'password',
        'name_first' : 'Benjamin',
        'name_last' : 'Long',
    })
    
    benjamin = user0.json()

    reg_uid = benjamin['u_id']
    reg_token = benjamin['token']
    assert reg_uid == 0
    
    reg_token = benjamin['token']
    
    logout = requests.post(f'{url}/auth/logout', json={
        'token' : reg_token
    })
      
    r = requests.post(f'{url}/auth/login', json={
        'email' : 'Benjamin@email.com',
        'password' : 'password',
    })   

    login = r.json()

    assert login['u_id'] == reg_uid
    assert login['token'] == reg_token
    


def test_auth_login_twice(url):

    # Clear data space
    requests.delete(f'{url}/clear')

    # Register users
    user0 = requests.post(f'{url}/auth/register', json={
        'email' : 'Benjamin@email.com',
        'password' : 'password',
        'name_first' : 'Benjamin',
        'name_last' : 'Long',
    })
    benjamin = user0.json()

    logout_return = requests.post(f'{url}/auth/logout', json={
        'token' : benjamin['token']
    })

    login = requests.post(f'{url}/auth/login', json={
        'email' : 'Benjamin@email.com',
        'password' : 'password',
    }) # logged in for the first time

    r = requests.post(f'{url}/auth/login', json={
        'email' : 'Benjamin@email.com',
        'password' : 'password',
    }) # trying to login for 2nd time in a row

    payload = r.json()
    assert payload['code'] == 400
    
      
def test_auth_login_invalid_password(url):
    
    # Clear data space
    requests.delete(f'{url}/clear')

    # Register users
    user0 = requests.post(f'{url}/auth/register', json={
        'email' : 'Benjamin@email.com',
        'password' : 'password',
        'name_first' : 'Benjamin',
        'name_last' : 'Long',
    })
    benjamin = user0.json()

    logout_return = requests.post(f'{url}/auth/logout', json={
        'token' : benjamin['token']
    })

    r = requests.post(f'{url}/auth/login', json={
        'email' : 'Benjamin@email.com',
        'password' : 'invalidpassword',
    })

    payload = r.json()

    assert payload['code'] == 400

    
def test_auth_login_doesnt_exist(url):   
    
    # Clear data space
    requests.delete(f'{url}/clear')

    # Email was never registered before login
    r = requests.post(f'{url}/auth/login', json={
        'email' : 'Benjamin@email.com',
        'password' : 'password',
    })

    payload = r.json()

    assert payload['code'] == 400
    

