from url_fixture import url
import pytest
import requests

@pytest.fixture
# def initialisation(url):
#     # Clear data space
#     requests.delete(f'{url}/clear')

#     # Register users
#     user0 = requests.post(f'{url}/auth/register', json={
#         'email' : 'Benjamin@email.com',
#         'password' : 'password',
#         'name_first' : 'Benjamin',
#         'name_last' : 'Long',
#     })
#     benjamin = user0.json()
#     user1 = requests.post(f'{url}/auth/register', json={
#         'email' : 'Ross@email.com',
#         'password' : 'password',
#         'name_first' : 'Ross',
#         'name_last' : 'Short',
#     })
#     ross = user1.json()

#     # Create channels
#     channel0 = requests.post(f'{url}/channels/create', json={
#         'token' : benjamin['token'],
#         'name' : 'channel0',
#         'is_public' : True,
#     })
#     channel0_id = channel0.json()
#     channel1 = requests.post(f'{url}/channels/create', json={
#         'token' : benjamin['token'],
#         'name' : 'channel1',
#         'is_public' : True,
#     })
#     channel1_id = channel1.json()

#     # Place users into relevant channels
#     requests.post(f'{url}/channel/invite', json={
#         'token' : benjamin['token'],
#         'channel_id' : channel0_id['channel_id'],
#         'u_id' : ross['u_id'],
#     })
#     return benjamin, ross, channel0_id, channel1_id
