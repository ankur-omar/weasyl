"""
Test suite for: resetpassword.py::def force(userid, form):
"""
import pytest

from weasyl.test import db_utils
from weasyl import resetpassword, login
from weasyl.error import WeasylError


class Bag(object):
    def __init__(self, **kw):
        for kv in kw.items():
            setattr(self, *kv)


def test_forcing_password_reset_with_mismatched_pw_fails():
    user_id = db_utils.create_user()
    password = '01234567890123'
    form = Bag(password=password, passcheck='1234567890987')
    with pytest.raises(WeasylError) as err:
        resetpassword.force(user_id, form)
    assert 'passwordMismatch' in str(err)


def test_forcing_password_reset_with_too_short_length_fails():
    user_id = db_utils.create_user()
    password = ''
    for i in range(0, login._PASSWORD):
        form = Bag(password=password, passcheck=password)
        with pytest.raises(WeasylError) as err:
            resetpassword.force(user_id, form)
        assert 'passwordInsecure' in str(err)
        password += 'a'


def test_verify_success_if_correct_information_provided():
    user_name = "testForce0003"
    user_id = db_utils.create_user(password='passwordpassword', username=user_name)
    password = '01234567890123'
    form = Bag(password=password, passcheck=password)
    resetpassword.force(user_id, form)
    result = login.authenticate_bcrypt(username=user_name, password=password, session=False)
    assert result == (user_id, None)
