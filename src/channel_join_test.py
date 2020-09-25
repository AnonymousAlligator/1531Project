from channel import channel_join
import error
import pytest

def test_channel_join_success():
    token = "Benjamin"
    channel_id = 1
    channel_join(token, channel_id)

def test_channel_join_invalid_channel():
    #The channel doesn't exist
    #This should throw InputError
    token = "Benjamin"
    channel_id = 51254
    with pytest.raises(error.InputError):
        assert channel_join(token, channel_id)

def test_channel_join_not_a_member():
    #Channel is private i.e. user is not admin
    #This should throw AccessError
    token = "Benjamin"
    channel_id = 2
    with pytest.raises(error.AccessError):
        assert channel_join(token, channel_id)