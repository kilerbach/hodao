"""
Created on 2014-9-2

@author: ilcwd
"""
import json
import logging

import flask

application = flask.Flask(__name__)

spy_logger = logging.getLogger('hodao.spy')


class C(object):
    DEBUG = False
    SERVER_SIGNATURE_KEY = None
    WECHAT_TOKEN = None
    SERVER_SESSION_KEY = None

    LOGIN_URL_EXPIRES = None
    SERVER_LOGIN_URL = None
    DB_FILE = None
    SERVER_MANAGEMENT_MAGIC_WORD = None
    WECHAT_API = None

    @classmethod
    def load_config(cls, config_file):
        content = {}
        with open(config_file, 'r') as f:
            content = json.loads(f.read())

        for k, v in cls.__dict__.iteritems():
            if k.startswith('_') or k == 'load_config':
                continue

            setattr(cls, k, content[k])






