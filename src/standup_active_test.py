from channel import channel_invite
from channels import channels_create
from auth import auth_register
from standup import standup_start, standup_active
from other import clear
import time
import error
import pytest

# Setting up all the variables needed for test to run ############################################
def initialisation():
    clear()
    Benjamin = auth_register("Benjamin@email.com", "password", "Benjamin", "Long")  # ID = 0
    Ross = auth_register("Ross@email.com", "password", "Ross", "Short")             # ID = 1
    Alex = auth_register("Alex@email.com", "password", "Alex", "Smith")             # ID = 2
    James = auth_register("James@email.com", "password", "James", "Smith")          # ID = 3

    # Channel1 is a private channel
    channel_id0 = channels_create(Benjamin['token'], "Channel0", True)  # ID = 0
    channel_id1 = channels_create(Ross['token'], "Channel1", False)     # ID = 1
    
    #Benjamin and Alex in channel 0
    channel_invite(Benjamin['token'], channel_id0['channel_id'], Alex['u_id'])
    # Ross and Alex in channel 1
    channel_invite(Ross['token'], channel_id1['channel_id'], Alex['u_id'])
    return Benjamin, Ross, Alex, James, channel_id0, channel_id1
##################################################################################################

def test_standup_active_public():
    Benjamin, _, Alex, _, channel_id0, _ = initialisation()
    # Standup should last for 2 seconds
    end_time = standup_start(Benjamin['token'],channel_id0['channel_id'], 2)
    time.sleep(1)
    assert standup_active(Benjamin['token'],channel_id0['channel_id']) == {'is_active': True, 'time_finish': end_time['time_finish']}
    assert standup_active(Alex['token'],channel_id0['channel_id']) == {'is_active': True, 'time_finish': end_time['time_finish']}
    time.sleep(1.5)
    assert standup_active(Benjamin['token'],channel_id0['channel_id']) == {'is_active': False, 'time_finish': None}
    assert standup_active(Alex['token'],channel_id0['channel_id']) == {'is_active': False, 'time_finish': None}

def test_standup_active_private():
    _, Ross, Alex, _, _, channel_id1 = initialisation()
    # Standup should last for 2 seconds
    end_time = standup_start(Ross['token'],channel_id1['channel_id'], 2)
    time.sleep(1)
    assert standup_active(Ross['token'],channel_id1['channel_id']) == {'is_active': True, 'time_finish': end_time['time_finish']}
    assert standup_active(Alex['token'],channel_id1['channel_id']) == {'is_active': True, 'time_finish': end_time['time_finish']}
    time.sleep(1.5)
    assert standup_active(Ross['token'],channel_id1['channel_id']) == {'is_active': False, 'time_finish': None}
    assert standup_active(Alex['token'],channel_id1['channel_id']) == {'is_active': False, 'time_finish': None}

def test_standup_active_not_member():
    Benjamin, _, _, James, channel_id0, _ = initialisation()
    # Standup should last for 2 seconds
    standup_start(Benjamin['token'],channel_id0['channel_id'], 2)
    time.sleep(1)
    with pytest.raises(error.AccessError):
        standup_active(James['token'],channel_id0['channel_id'])
    time.sleep(1.5)
    with pytest.raises(error.AccessError):
        standup_active(James['token'],channel_id0['channel_id'])

def test_standup_active_invalid_channel():
    Benjamin, _, _, _, channel_id0, _ = initialisation()
    standup_start(Benjamin['token'],channel_id0['channel_id'], 2)
    time.sleep(1)
    with pytest.raises(error.InputError):
        standup_start(Benjamin['token'],5, 2)

def test_standup_active_invalid_token():
    Benjamin, _, _, _, channel_id0, _ = initialisation()
    standup_start(Benjamin['token'],channel_id0['channel_id'], 2)
    time.sleep(1)
    with pytest.raises(error.AccessError):
        standup_active('Boop',channel_id0['channel_id'])
