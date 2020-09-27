'''
InputError when any of:
Email entered is not a valid email using the method provided here (unless you feel you have a better method).
Email address is already being used by another user
'''
from user import user_profile
from error import InputError
import auth
import pytest

def user_profile_setemail_test():
  
  #TODO: clear data