from url_fixture import url
from flask import Flask, request, send_from_directory, render_template
import pytest
import requests
import json

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
        'x_start' : 0,
        'y_start' : 0,
        'x_end' : 200,
        'y_end' : 200,
    })
    payload = r.status_code
    assert payload == 200

def test_user_profile_photo_width_too_large(url, initialisation):
    user0 = initialisation
    r = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token' : user0['token'],
        'img_url' : 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Teemo_0.jpg',
        'x_start' : 0,
        'y_start' : 0,
        'x_end' : 1220,
        'y_end' : 717,
    })
    payload = r.status_code
    assert payload == 400

def test_user_profile_photo_length_too_large(url, initialisation):
    user0 = initialisation
    r = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token' : user0['token'],
        'img_url' : 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Teemo_0.jpg',
        'x_start' : 0,
        'y_start' : 0,
        'x_end' : 1215,
        'y_end' : 720,
    })
    payload = r.status_code
    assert payload == 400

def test_user_profile_photo_not_jpeg(url, initialisation):
    user0 = initialisation
    r = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token' : user0['token'],
        'img_url' : 'https://static.wikia.nocookie.net/leagueoflegends/images/d/d6/Teemo_Render.png/revision/latest?cb=20190112183654',
        'x_start' : 0,
        'y_start' : 0,
        'x_end' :200,
        'y_end' : 200,
    })
    payload = r.status_code
    assert payload == 400

def test_user_profile_photo_zero_width(url, initialisation):
    user0 = initialisation
    r = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token' : user0['token'],
        'img_url' : 'https://static.wikia.nocookie.net/leagueoflegends/images/d/d6/Teemo_Render.png/revision/latest?cb=20190112183654',
        'x_start' : 0,
        'y_start' : 0,
        'x_end' : 0,
        'y_end' : 200,
    })
    payload = r.status_code
    assert payload == 400

def test_user_profile_photo_zero_height(url, initialisation):
    user0 = initialisation
    r = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token' : user0['token'],
        'img_url' : 'https://static.wikia.nocookie.net/leagueoflegends/images/d/d6/Teemo_Render.png/revision/latest?cb=20190112183654',
        'x_start' : 0,
        'y_start' : 0,
        'x_end' : 200,
        'y_end' : 0,
    })
    payload = r.status_code
    assert payload == 400

def test_user_profile_photo_negative_xstart(url, initialisation):
    user0 = initialisation
    r = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token' : user0['token'],
        'img_url' : 'https://static.wikia.nocookie.net/leagueoflegends/images/d/d6/Teemo_Render.png/revision/latest?cb=20190112183654',
        'x_start' : -200,
        'y_start' : 0,
        'x_end' : 200,
        'y_end' : 100,
    })
    payload = r.status_code
    assert payload == 400

def test_user_profile_photo_negative_ystart(url, initialisation):
    user0 = initialisation
    r = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token' : user0['token'],
        'img_url' : 'https://static.wikia.nocookie.net/leagueoflegends/images/d/d6/Teemo_Render.png/revision/latest?cb=20190112183654',
        'x_start' : 0,
        'y_start' : -50,
        'x_end' : 200,
        'y_end' : 100,
    })
    payload = r.status_code
    assert payload == 400

def test_user_profile_photo_negative_yend(url, initialisation):
    user0 = initialisation
    r = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token' : user0['token'],
        'img_url' : 'https://static.wikia.nocookie.net/leagueoflegends/images/d/d6/Teemo_Render.png/revision/latest?cb=20190112183654',
        'x_start' : 0,
        'y_start' : 0,
        'x_end' : 200,
        'y_end' : -40,
    })
    payload = r.status_code
    assert payload == 400

def test_user_profile_photo_negative_xend(url, initialisation):
    user0 = initialisation
    r = requests.post(f'{url}/user/profile/uploadphoto', json={
        'token' : user0['token'],
        'img_url' : 'https://static.wikia.nocookie.net/leagueoflegends/images/d/d6/Teemo_Render.png/revision/latest?cb=20190112183654',
        'x_start' : 0,
        'y_start' : 0,
        'x_end' : -80,
        'y_end' : 100,
    })
    payload = r.status_code
    assert payload == 400

