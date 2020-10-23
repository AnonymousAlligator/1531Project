from url_fixture import url
import pytest
import requests

@pytest.fixture
def initialisation(url):

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

    return benjamin, ross

def test_auth_register1(url, initialisation):

    # Clear data space
    requests.delete(f'{url}/clear')

    # When an email has a valid format but not registered yet
    # Register new user
    benjamin, ross = initialisation
    
    assert benjamin['u_id'] == 0
    assert ross['u_id'] == 1
    

def test_valid_but_already_registered(url, initialisation):


    # When the email has a valid format but is already registered, even if 
    # with a different name
    r = requests.post(f'{url}/auth/register', json={
        'email' : 'Benjamin@email.com',
        'password' : 'password',
        'name_first' : 'Kate',
        'name_last' : 'Wong',
    })

    payload = r.json()

    assert payload['code'] == 400    

def test_register_after_clear(url, initialisation):

    # Clear data space
    requests.delete(f'{url}/clear')

    # When registered with same email after data is cleared
    benjamin,_ = initialisation
    
    assert benjamin['u_id'] == 0
def test_invalid_format_1(url, initialisation):
    
    # Clear data space
    requests.delete(f'{url}/clear')

    # When email doesn't contain substring before @
    r = requests.post(f'{url}/auth/register', json={
        'email' : 'email.com',
        'password' : 'jamaica45678',
        'name_first' : 'Elena',
        'name_last' : 'Drake',
    })

    payload = r.json()

    assert payload['code'] == 400 
    

def test_invalid_format_2(url, initialisation):
    
    # Clear data space
    requests.delete(f'{url}/clear')

    # When email does not contain ".com" in the end
    
    r = requests.post(f'{url}/auth/register', json={
        'email' : 'invalid@email',
        'password' : 'fortunehunter',
        'name_first' : 'Victor',
        'name_last' : 'Sullivan',
    })

    payload = r.json()

    assert payload['code'] == 400 
    
    
def test_invalid_format_3(url, initialisation):
    
    # Clear data space
    requests.delete(f'{url}/clear')

    # when email contains 2 @s
    
    r = requests.post(f'{url}/auth/register', json={
        'email' : 'invalid@@email',
        'password' : 'potatooblivion',
        'name_first' : 'Nick',
        'name_last' : 'Mitch',
    })

    payload = r.json()

    assert payload['code'] == 400 
    

def test_invalid_format_4(url, initialisation):
    
    # Clear data space
    requests.delete(f'{url}/clear')

    #When email doesn't contain "@example.com" type substring
    
    r = requests.post(f'{url}/auth/register', json={
        'email' : 'eeeemail',
        'password' : 'iamsotiredloool',
        'name_first' : 'Radine',
        'name_last' : 'Noss',
    })

    payload = r.json()

    assert payload['code'] == 400 

def test_invalid_format_5(url, initialisation):
    
    # Clear data space
    requests.delete(f'{url}/clear')

    #When email is empty
    
    r = requests.post(f'{url}/auth/register', json={
        'email' : '',
        'password' : 'iamsotiredloool',
        'name_first' : 'Radine',
        'name_last' : 'Noss',
    })

    payload = r.json()

    assert payload['code'] == 400 

    

def test_firstname_too_long(url, initialisation):
    
    # Clear data space
    requests.delete(f'{url}/clear')

    
    # When the first name is too long
    
    r = requests.post(f'{url}/auth/register', json={
        'email' : 'valid@email.com',
        'password' : 'wanttosleep321',
        'name_first' : 'toomanychars'*20,
        'name_last' : 'Noss',
    })

    payload = r.json()

    assert payload['code'] == 400 


def test_firstname_too_short(url, initialisation):
    
    # Clear data space
    requests.delete(f'{url}/clear')

    
    # When the first name is too short
    
    r = requests.post(f'{url}/auth/register', json={
        'email' : 'valid@email.com',
        'password' : 'wanttosleep321',
        'name_first' : '',
        'name_last' : 'Potter',
    })

    payload = r.json()

    assert payload['code'] == 400 
    
def test_firstname_empty_space(url, initialisation):
    
    # Clear data space
    requests.delete(f'{url}/clear')

    
    # When the first name is too short
    
    r = requests.post(f'{url}/auth/register', json={
        'email' : 'valid@email.com',
        'password' : 'wanttosleep321',
        'name_first' : '                ',
        'name_last' : 'Potter',
    })

    payload = r.json()

    assert payload['code'] == 400 

def test_lastname_too_long(url, initialisation):
    
    # Clear data space
    requests.delete(f'{url}/clear')

    
    # When the last name is too short
    
    r = requests.post(f'{url}/auth/register', json={
        'email' : 'valid@email.com',
        'password' : 'wanttosleep321',
        'name_first' : 'Harry',
        'name_last' : 'Potter'*30,
    })

    payload = r.json()

    assert payload['code'] == 400 
def test_lastname_too_short(url, initialisation):
    
    # Clear data space
    requests.delete(f'{url}/clear')

    
    # When the last name is too short
    
    r = requests.post(f'{url}/auth/register', json={
        'email' : 'valid@email.com',
        'password' : 'wanttosleep321',
        'name_first' : 'Harry',
        'name_last' : '',
    })

    payload = r.json()

    assert payload['code'] == 400 


def test_lastname_empty_space(url, initialisation):
    
    # Clear data space
    requests.delete(f'{url}/clear')

    
    # When the last name is too short
    
    r = requests.post(f'{url}/auth/register', json={
        'email' : 'valid@email.com',
        'password' : 'wanttosleep321',
        'name_first' : 'Harry',
        'name_last' : '                   ',
    })

    payload = r.json()

    assert payload['code'] == 400 

def test_password_too_short(url, initialisation):
    
    # Clear data space
    requests.delete(f'{url}/clear')

    
    # When the last name is too short
    
    r = requests.post(f'{url}/auth/register', json={
        'email' : 'valid@email.com',
        'password' : 'smol',
        'name_first' : 'Harry',
        'name_last' : 'Potterrrrrr',
    })

    payload = r.json()

    assert payload['code'] == 400 

