# coding: utf8
#
# hoshop - restfulapi
# 
# Author: ilcwd 
# Create: 14/12/30
#

import functools

import flask
from flask import jsonify, request, blueprints

from hodao.core import application
from hodao.models import order, contact

app = blueprints.Blueprint('api', __name__)


def check_login(f):
    @functools.wraps(f)
    def _wrapper(*a, **kw):
        print flask.request.headers
        return f(*a, **kw)

    return _wrapper


@app.route('/order/create', methods=['POST'])
@check_login
def create_order():
    return jsonify({'s':'hello'})


@app.route('/order/sync', methods=['POST'])
@check_login
def sync_orders():
    return jsonify({'s':'hello'})