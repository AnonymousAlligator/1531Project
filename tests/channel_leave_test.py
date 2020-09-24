from src.channel import channel_leave
import src.error
import pytest

def test_channel_leave_success():
    token = "Benjamin"
    channel_id = 1
    channel_leave(token, channel_id)

def test_channel_leave_invalid_channel():
    #The channel doesn't exist
    #This should throw InputError
    token = "Benjamin"
    channel_id = 51254
    with pytest.raises(src.error.InputError) as e:
        assert channel_leave(token, channel_id)
        assert 'The channel does not exist' in str(e.value)

def test_channel_leave_not_a_member():
    #User is not part of this channel
    #This should throw AccessError
    token = "Benjamin"
    channel_id = 2
    with pytest.raises(src.error.AccessError) as e:
        assert channel_leave(token, channel_id)
        assert 'You are not part of this channel' in str(e.value)