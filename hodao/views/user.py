# coding:utf8
"""

Author: ilcwd
"""

import flask
from flask import request
# noinspection PyUnresolvedReferences
from flask.ext.paginate import Pagination

from hodao.core import application, C
from hodao import util


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
