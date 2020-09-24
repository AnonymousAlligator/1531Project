from channel import channel_leave
import error
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
    with pytest.raises(error.InputError):
        assert channel_leave(token, channel_id)

def test_channel_leave_not_a_member():
    #User is not part of this channel
    #This should throw AccessError
    token = "Benjamin"
    channel_id = 2
    with pytest.raises(error.AccessError):
        assert channel_leave(token, channel_id)