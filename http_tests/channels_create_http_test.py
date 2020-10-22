from url_fixture import url
import pytest
import requests

@pytest.fixture
def initialisation(url):
    # Clear data space
    requests.delete(f'{url}/clear')

    #register test users
    user0 = requests.post(f'{url}/auth/register', json={
        "email" : "testemail0@email.com",
        "password" : "valid_pw0",
        "name_first" : "Hayden",
        "name_last" : "Jacobs",
    })
    user0 = user0.json()

    channel_name1 = "Main Channel"
    channel_name2 = "abcdefhijklmnopqrst"
    channel_name3 = "abcdefhijklmnopqrstuvwxyz"

    return user0, channel_name1, channel_name2, channel_name3

def test_channels_create_lessthan20(url, initialisation):
    user0, channel_name1, _, _, = initialisation
    r = requests.post(f'{url}/channels/create', json={
        'token' : user0['token'],
        'name' : channel_name1,
        'is_public' : True,      
    })
    payload = r.json()
    assert payload == {}

def test_channels_create_exactly20(url, initialisation):
    user0, _, channel_name2, _, = initialisation
    r = requests.post(f'{url}/channels/create', json={
        'token' : user0['token'],
        'name' : channel_name2,
        'is_public' : True,      
    })
    payload = r.json()
    assert payload == {}

def test_channels_create_morethan20(url, initialisation):
    user0, _, _, channel_name3, = initialisation
    r = requests.post(f'{url}/channels/create', json={
        'token' : user0['token'],
        'name' : channel_name3,
        'is_public' : True,      
    })
    payload = r.json()
    assert payload == {}

def test_channels_create_public(url, initialisation):
    user0, _, channel_name2, _, = initialisation
    r = requests.post(f'{url}/channels/create', json={
        'token' : user0['token'],
        'name' : channel_name2,
        'is_public' : True,      
    })
    payload = r.json()
    assert payload == {}

def test_channels_create_private(url, initialisation):
    user0, channel_name1, _, _, = initialisation
    r = requests.post(f'{url}/channels/create', json={
        'token' : user0['token'],
        'name' : channel_name1,
        'is_public' : False,      
    })
    payload = r.json()
    assert payload == {}

def test_channels_create_invalidtoken(url, initialisation):
    _, channel_name1, _, _, = initialisation
    r = requests.post(f'{url}/channels/create', json={
        'token' : 'Hello',
        'name' : channel_name1,
        'is_public' : True,      
    })
    payload = r.json()
    assert payload == {}