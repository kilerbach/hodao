# coding:utf8
"""

Author: ilcwd
"""

import flask
from wechat.server import (
    WechatApplication,
    text_reply,

    EVENT_SUBSCRIBE,
    MSG_TEXT,
)


from hodao.core import application, C
from hodao import util


wechatapp = WechatApplication(application, '/api/wechat', C.WECHAT_TOKEN)


@wechatapp.text('A')
@wechatapp.text('a')
def express_service():
    from_user = flask.g.wechat['ToUserName']
    to_user = flask.g.wechat['FromUserName']

    content = (
        """【<a href="%s">猛戳蓝字</a>】\n"""
        """提交订单，查询Ho单"""
    ) % (util.make_auth_url(to_user, redirect='/order/create'),)
    return text_reply(from_user, to_user, content)


@wechatapp.message(MSG_TEXT)
@wechatapp.event(EVENT_SUBSCRIBE)
def help_msg():
    from_user = flask.g.wechat['ToUserName']
    to_user = flask.g.wechat['FromUserName']

    content = (
        """星海用Ho道！生活无难度～/礼物/礼物\n"""
        """Ho道 服务如下：\n"""
        """A. 快递代理\n"""
        """B. 美食大搜罗\n"""
        """C. Ho道大喇叭\n"""
        """D. 寻求合作\n"""
        """如回复：A\n"""
    )
    return text_reply(from_user, to_user, content)