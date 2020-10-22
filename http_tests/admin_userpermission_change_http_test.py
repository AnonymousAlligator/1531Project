
from url_fixture import url
import pytest
import requests

@pytest.fixture
def test_admin_userpermission_change_successtoowner(url):
    #clear data
    requests.delete(f'{url}/clear')
    
    #register test users
    user0 = requests.post(f'{url}/auth/register', json={
        "email" : "testemail0@email.com",
        "password" : "valid_pw0",
        "name_first" : "Hayden",
        "name_last" : "Jacobs",
    })
    user0 = user0.json()

    user1 = requests.post(f'{url}/auth/register', json={
        "email" : "testemail1@email.com",
        "password" : "valid_pw1",
        "name_first" : "Jayden",
        "name_last" : "Haycobs",
    })
    user1 = user1.json()

    r = requests.post(f'{url}/admin/userpermission/change', json={
        'token' : user0['token'],
        'u_id' : user1['u_id'],
        'permission_id' : 1,
    })
    payload = r.json()

    assert payload == {}