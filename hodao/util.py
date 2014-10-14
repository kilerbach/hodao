# coding:utf8
"""

Author: ilcwd
"""
import hashlib
import time
import urllib

from hodao.core import C


class HodaoException(Exception):
    pass


class NeedLoginException(HodaoException):
    pass


class NeedSuperException(HodaoException):
    pass


def sign_request(*a):
    params = list(a)
    params.append(C.SERVER_SIGNATURE_KEY)

    return hashlib.sha1(''.join(sorted(map(str, params)))).hexdigest()


def make_auth_url(user, redirect='/order/create'):
    u = str(user)
    t = str(int(time.time()))

    s = sign_request(u, t)

    query_string = {
        'u': u,
        't': t,
        's': s,
        'next': redirect,
    }
    return C.SERVER_LOGIN_URL + '?' + urllib.urlencode(query_string)


def valid_request(s, u, t):
    # expired
    if abs(int(t) - time.time()) > C.LOGIN_URL_EXPIRES:
        return False

    expect = sign_request(u, t)

    return expect == str(s)
