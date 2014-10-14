# coding:utf8
"""

Author: ilcwd
"""

import flask
from flask import request

from hodao.core import application, C
from hodao import util
from hodao.util import NeedLoginException

user = flask.Blueprint('user', __name__)


@user.route('/', methods=['GET', 'POST'])
def login():
    u = request.values.get('u')
    t = request.values.get('t')
    s = request.values.get('s')
    redirect_url = request.values.get('next')

    if not (u and t and s) or not util.valid_request(s, u, t):
        raise NeedLoginException()

    flask.session['user'] = u
    flask.session['admin'] = 0
    if redirect_url:
        return flask.redirect(redirect_url)

    return flask.redirect('/order/create')


@user.route('/' + C.SERVER_MANAGEMENT_MAGIC_WORD)
def admin_login():
    flask.session['user'] = ''
    flask.session['admin'] = 1
    return flask.redirect('/order/manage')


@user.route('/publicuser')
def public_login():
    flask.session['user'] = 'publicuser'
    flask.session['admin'] = 0
    return flask.redirect('/order')


application.register_blueprint(user, url_prefix='/login')