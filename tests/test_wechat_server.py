# coding:utf8
"""

Author: ilcwd
"""

from base import *


def test_wechat_api():
    # default empty response
    assert_equal(wechat_api_rpc(), '')

    # invalid token
    assert_equal(wechat_api_rpc(server_token='a_wrong_token'), '')

    # express url
    for msg in ['A', 'a']:
        req_a = TextRequest(msg)
        resp_a = wechat_api_rpc(post=req_a.to_string())
        resp_a = read_xml(resp_a)

        assert_equal('text', resp_a['MsgType'])
        assert u'猛戳蓝字' in resp_a['Content'], resp_a['Content']

    # a subscribe event
    req_subscibe = EventRequest()
    resp_help = wechat_api_rpc(post=req_subscibe.to_string())
    resp_help = read_xml(resp_help)
    assert_equal('text', resp_help['MsgType'])
    assert u'星海用Ho道！生活无难度' in resp_help['Content'], resp_help['Content']


def main():
    test_wechat_api()

    print "fin"


if __name__ == '__main__':
    main()
