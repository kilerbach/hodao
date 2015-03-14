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

    phone = request.form['phone']
    company = request.form['company']
    name = request.form['name']
    amount = int(request.form.get('amount', 1))
    save_contact = request.form.get('savecontact', 'off') == 'on'

    user = flask.session['user']
    orderids = order.create_order(user, name, company, phone, amount)

    address = request.form.get('address')
    if orderids and address:
        order.add_address_to_orders(address, orderids)

    if save_contact:
        contact.create_contact(user, name, phone)

    return jsonify({'status': 0})


@app.route('/order/sync', methods=['POST'])
@check_login
def sync_orders():
    return jsonify({'s':'hello'})