from user import user_profile_uploadphoto
from auth import auth_register
from other import clear
from error import InputError
import pytest

@pytest.fixture
def initialisation():
    #clear data
    clear()
    #register test users
    user0 = auth_register("ben@email.com","password","ben","long")
    return user0

def test_user_profile_photo_width_too_large(initialisation):
    user0 = initialisation
    with pytest.raises(InputError):
        user_profile_uploadphoto(user0['token'],'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Teemo_0.jpg',0,0,1220,717)

def test_user_profile_photo_length_too_large(initialisation):
    user0 = initialisation
    with pytest.raises(InputError):
        user_profile_uploadphoto(user0['token'],'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Teemo_0.jpg',0,0,1215,720)

def test_user_profile_photo_not_jpeg(initialisation):
    user0 = initialisation
    with pytest.raises(InputError):
        user_profile_uploadphoto(user0['token'],'https://static.wikia.nocookie.net/leagueoflegends/images/d/d6/Teemo_Render.png/revision/latest?cb=20190112183654',0,0,200,200)

def test_user_profile_photo_zero_width(initialisation):
    user0 = initialisation
    with pytest.raises(InputError):
        user_profile_uploadphoto(user0['token'],'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Teemo_0.jpg',0,0,0,200)

def test_user_profile_photo_zero_height(initialisation):
    user0 = initialisation
    with pytest.raises(InputError):
        user_profile_uploadphoto(user0['token'],'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Teemo_0.jpg',0,0,200,0)

def test_user_profile_photo_negative_xstart(initialisation):
    user0 = initialisation
    with pytest.raises(InputError):
        user_profile_uploadphoto(user0['token'],'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Teemo_0.jpg',-200,0,200,100)

def test_user_profile_photo_negative_ystart(initialisation):
    user0 = initialisation
    with pytest.raises(InputError):
        user_profile_uploadphoto(user0['token'],'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Teemo_0.jpg',0,-50,200,100)

def test_user_profile_photo_negative_yend(initialisation):
    user0 = initialisation
    with pytest.raises(InputError):
        user_profile_uploadphoto(user0['token'],'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Teemo_0.jpg',0,0,200,-40)

def test_user_profile_photo_negative_xend(initialisation):
    user0 = initialisation
    with pytest.raises(InputError):
        user_profile_uploadphoto(user0['token'],'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Teemo_0.jpg',0,0,-80,100)
