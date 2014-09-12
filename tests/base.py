# coding:utf8
"""

Author: ilcwd
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))
import time
import hashlib
import urllib
import random
import xml.etree.cElementTree

import werkzeug.test

from wsgiapp import application, C

app = application
app.debug = True


CLIENT = werkzeug.test.Client(app)


################################
# Utils
################################
def utf8_str(s):
    if isinstance(s, unicode):
        return s.encode('utf8')
    elif isinstance(s, str):
        return s

    return str(s)


def read_xml(xmlstr):
    """Simple xml to dict function.

    Aim for wechat request parsing.
    """
    if not xmlstr:
        return {}

    def _read_node(xmlnodes):
        _result = {}
        for item in xmlnodes:
            children = item.getchildren()
            if children:
                _result[item.tag] = _read_node(children)
            else:
                _result[item.tag] = item.text
        return _result

    return _read_node(xml.etree.cElementTree.fromstring(xmlstr))


def assert_equal(a, b):
    assert a == b, ("Expect `%s`, but `%s`." % (a, b))


def timestamp():
    return int(time.time())


def randomstr():
    return os.urandom(8).encode('hex')


def signature(token):
    ts = timestamp()
    nonce = randomstr()
    sign = hashlib.sha1(''.join(sorted(map(str, [token, ts, nonce])))).hexdigest()
    return ts, nonce, sign


def wechat_api_rpc(path=C.WECHAT_API, post=None, server_token=C.WECHAT_TOKEN):
    # werkzeug.test.Client donot set REMOTE_ADDR!
    environ_overrides = {'REMOTE_ADDR': '127.0.0.1'}

    method = 'POST' if post else 'GET'

    # sign request
    ts, nonce, sign = signature(server_token)
    path = path + '?' + urllib.urlencode({'timestamp': ts, 'nonce': nonce, 'signature': sign})

    # open request
    resp, status, headers = CLIENT.open(path=path, method=method,
                                        content_type='application/xml',
                                        data=post,
                                        environ_overrides=environ_overrides)

    # validation
    assert status.startswith('200'), status
    result = ''.join(resp)
    return result


class BaseRequest(object):
    _TEMPLATE = None

    def __init__(self):
        self.to_user = randomstr()
        self.from_user = randomstr()
        self.create_time = str(timestamp())
        self.msg_id = str(random.randint(0, 0xFFFFFFFFFFFFFFFF))

    def to_string(self):
        return self._TEMPLATE % self.__dict__


class EventRequest(BaseRequest):
    _TEMPLATE = """<xml><ToUserName><![CDATA[%(to_user)s]]></ToUserName>
<FromUserName><![CDATA[%(from_user)s]]></FromUserName>
<CreateTime>%(create_time)s</CreateTime>
<MsgType><![CDATA[%(msg_type)s]]></MsgType>
<Event><![CDATA[%(event)s]]></Event>
</xml>"""

    def __init__(self):
        super(EventRequest, self).__init__()
        self.msg_type = 'event'
        self.event = 'subscribe'


class TextRequest(BaseRequest):
    _TEMPLATE = """<xml><ToUserName><![CDATA[%(to_user)s]]></ToUserName>
<FromUserName><![CDATA[%(from_user)s]]></FromUserName>
<CreateTime>%(create_time)s</CreateTime>
<MsgType><![CDATA[%(msg_type)s]]></MsgType>
<Content><![CDATA[%(content)s]]></Content>
<MsgId>%(msg_id)s</MsgId>
</xml>"""

    def __init__(self, content):
        super(TextRequest, self).__init__()
        self.msg_type = 'text'
        self.content = content