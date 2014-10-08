# coding:utf8
"""

Author: ilcwd
"""

import flask
from flask import render_template, request
# noinspection PyUnresolvedReferences
from flask.ext.paginate import Pagination

from hodao.core import application, C
from hodao import util


def render_login_page():
    return render_template(
        'error.html',
        msg=u'请先登录~',
        raw=u"""<p class="white-font">如何登陆？</p>
        <p class="white-font">请使用微信搜索公众号：
            <a class="rich_media_meta link nickname" href="weixin://addfriend/gh_073d2ed7bb43"
               id="post-user">Ho道</a>
        </p>
        <p class="white-font">关注成功后回复<b>A</b>就可以跳转至此页面。</p>
        """
    )


@application.route('/login', methods=['GET', 'POST'])
def login():
    u = request.values.get('u')
    t = request.values.get('t')
    s = request.values.get('s')
    redirect_url = request.values.get('next')

    if not (u and t and s) or not util.valid_request(s, u, t):
        return render_login_page()

    flask.session['user'] = u
    flask.session['admin'] = 0
    if redirect_url:
        return flask.redirect(redirect_url)

    return flask.redirect('/order/create')


@application.route('/login/' + C.SERVER_MANAGEMENT_MAGIC_WORD)
def admin_login():
    flask.session['user'] = ''
    flask.session['admin'] = 1
    return flask.redirect('/order/manage')


@application.route('/login/publicuser')
def public_login():
    flask.session['user'] = 'publicuser'
    flask.session['admin'] = 0
    return flask.redirect('/order')
