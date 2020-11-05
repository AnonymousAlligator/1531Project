from user import user_profile_uploadphoto
from error import InputError
from other import clear
from test_helpers import create_one_test_user
import pytest


def test_user_profile_photo_width_too_large():
    clear()
    test_user0 = create_one_test_user()
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(test_user0['token'], 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Teemo_0.jpg', 0, 0, 1220, 717) == {}

def test_user_profile_photo_length_too_large():
    clear()
    test_user0 = create_one_test_user()
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(test_user0['token'], 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Teemo_0.jpg', 0, 0, 1215, 720) == {}

def test_user_profile_photo_not_jpeg():
    clear()
    test_user0 = create_one_test_user()
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(test_user0['token'], 'https://static.wikia.nocookie.net/leagueoflegends/images/d/d6/Teemo_Render.png/revision/latest?cb=20190112183654', 0, 0, 200, 200) == {}

def test_user_profile_photo_success():
    clear()
    test_user0 = create_one_test_user()
    assert user_profile_uploadphoto(test_user0['token'], 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Teemo_0.jpg', 600, 100, 1000, 400) == {}
