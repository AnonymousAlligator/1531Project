from url_fixture import url
from flask import Flask, request, send_from_directory
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
        'img_url' : 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Teemo_0.jpg',
        'x_start' : '600',
        'y_start' : '100',
        'x_end' :'1000',
        'y_end' : '400',
    })
    #payload = send_from_directory('static', f'{user0["token"]}.jpeg')
    payload = r.json()
    assert payload == {}
    


def test_user_profile_photo_width_too_large(url, initialisation):
    user0 = initialisation
    r = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token' : user0['token'],
        'img_url' : 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Teemo_0.jpg',
        'x_start' : '0',
        'y_start' : '0',
        'x_end' :'1220',
        'y_end' : '717',
    })
    payload = r.json()
    assert payload['code'] == 400