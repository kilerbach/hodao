# coding: utf8
#
# hoshop - session
# 
# Author: ilcwd 
# Create: 15/1/30
#
import uuid
import time
import json
import hashlib

import redis

from hodao.core import C

_redis_client = None

_DEFAULT_SESSION_EXPIRED_DAYS = 365
_SESSION_KEY_PREFIX = "SSN:"


class SESSION_TYPE:
    UNKNOW = 'u'
    DEVICE = 'd'


def _get_db():
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis(**C.SESSION_REDIS)

    return _redis_client


def _format_key_in_db(token):
    return _SESSION_KEY_PREFIX + hashlib.sha1(token).digest().encode('base64')[:-1]


def _generate_token(userid=0, expired_days=_DEFAULT_SESSION_EXPIRED_DAYS, session_type=SESSION_TYPE.UNKNOW):
    now = int(time.time())
    expires = now + _DEFAULT_SESSION_EXPIRED_DAYS*3600*24
    return "%s.%d-%d.%d.%s" % (session_type, now, expires, userid, uuid.uuid4().hex)


def _serialize_data(dictobj):
    return json.dumps({
        'data': dictobj,
    })


def _deserialize_data(data):
    try:
        return json.loads(data)['data']
    except (TypeError, ValueError, KeyError):
        return None


def create_session(userinfo, session_type=SESSION_TYPE.UNKNOW):
    """

    :param userinfo:
    :return: token
    """
    expires = _DEFAULT_SESSION_EXPIRED_DAYS
    token = _generate_token(userinfo['userid'], expires, session_type)
    db_key = _format_key_in_db(token)

    _get_db().setex(db_key, _serialize_data(userinfo), expires*24*3600)
    return token


def get_session(token):
    """
    :param token:
    :return: userinfo
    """

    db_key = _format_key_in_db(token)
    return _deserialize_data(_get_db().get(db_key))


def main():
    print "%s" % int(time.time())
    print create_session("")


if __name__ == '__main__':
    main()