# coding:utf8
"""

Author: ilcwd
"""
import functools

import flask

from hodao.util import NeedLoginException, NeedSuperException


def is_login():
    return bool(flask.session.get('user'))


def is_super():
    return bool(flask.session.get('admin'))


def check_login(func):
    @functools.wraps(func)
    def _wrapper(*a, **kw):
        if not is_login():
            raise NeedLoginException()

        return func(*a, **kw)

    return _wrapper


def check_login_or_super(func):
    @functools.wraps(func)
    def _wrapper(*a, **kw):
        if not (is_login() or is_super()):
            raise NeedLoginException()

        return func(*a, **kw)

    return _wrapper


def check_super(func):
    @functools.wraps(func)
    def _wrapper(*a, **kw):
        if not is_super():
            raise NeedSuperException()

        return func(*a, **kw)

    return _wrapper



