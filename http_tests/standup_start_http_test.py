from url_fixture import url
from time import sleep
import pytest
import requests

def initialisation(url):
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
    user1 = requests.post(f'{url}/auth/register', json={
        'email' : 'Ross@email.com',
        'password' : 'password',
        'name_first' : 'Ross',
        'name_last' : 'Short',
    })
    ross = user1.json()

    # Create channels
    channel0 = requests.post(f'{url}/channels/create', json={
        'token' : benjamin['token'],
        'name' : 'channel0',
        'is_public' : True,
    })
    channel0_id = channel0.json()
    channel1 = requests.post(f'{url}/channels/create', json={
        'token' : benjamin['token'],
        'name' : 'channel1',
        'is_public' : True,
    })
    channel1_id = channel1.json()

    # Place users into relevant channels
    requests.post(f'{url}/channel/invite', json={
        'token' : benjamin['token'],
        'channel_id' : channel0_id['channel_id'],
        'u_id' : ross['u_id'],
    })
    return benjamin, ross, channel0_id, channel1_id

# check standup_start in 1 valid channel with no active standup works
def test_standup_start_one(url, initialisation):
  pass

def test_standup_start_two(url, initialisation):
  pass

# check for error when user tries to start 2 active standups in a channel
def test_standup_start_invalid_two(url, initialisation):
  pass

# check for error when user tries to start standup in invalid channel
def test_standup_start_invalid_channel(url, initialisation):
  pass
