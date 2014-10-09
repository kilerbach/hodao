# coding:utf8
"""

Author: ilcwd
"""
from collections import defaultdict

import flask
from flask import render_template, request
from flask_paginate import Pagination

from hodao.core import application
from hodao.models import order, contact
from hodao.models.base import ORDER_STATUS_MAPPING
from .util import check_login, check_super, check_login_or_super


@application.route('/')
@check_login
def index():
    user = flask.session['user']
    contacts = contact.query_contacts(user)
    return render_template('index.html', contacts=contacts)


@application.route('/order')
@check_login
def show_orders():
    user = flask.session['user']
    orders = order.query_orders(user)
    return render_template('orders.html', orders=orders)


@application.route('/order/manage', defaults={'page': 1})
@application.route('/order/manage/page/<int:page>')
@check_super
def manage_orders(page):

    per_page = 20
    total, orders = order.query_all_orders(page, per_page)
    date_express_orders = defaultdict(lambda: defaultdict(list))

    def _get_date(dt):
        return dt.strftime("%Y-%m-%d")

    for o in orders:
        date = _get_date(o.created_time)
        date_express_orders[date][o.company].append(o)

    result = []
    for d, ex_ords in sorted(date_express_orders.items(), reverse=True):
        for ex, ods in sorted(ex_ords.items()):
            result.append([(d, ex), sorted(ods, key=lambda x: x.created_time, reverse=True)])

    pagination = Pagination(page=page, per_page=per_page, total=total, bs_version=3)

    return render_template(
        'management.html',
        sorted_orders=result,
        order_status_mapping=ORDER_STATUS_MAPPING,
        pagination=pagination,
    )


@application.route('/order/create', methods=['GET', 'POST'])
@check_login
def create_order():
    if request.method == 'GET':
        return index()

    phone = request.form['phone']
    company = request.form['company']
    name = request.form['name']
    amount = int(request.form.get('amount', 1))
    save_contact = request.form.get('savecontact', 'off') == 'on'

    user = flask.session['user']
    order.create_order(user, name, company, phone, amount)

    if save_contact:
        contact.create_contact(user, name, phone)

    return flask.redirect('/order')


@application.route('/order/update', methods=['POST'])
@check_login_or_super
def update_order():
    order_id = request.form['order_id']
    status = request.form['status']

    # check permission
    user = flask.session.get('user')

    order.update_order(order_id, int(status), user or None)
    redirect_url = request.form.get('next')
    if redirect_url:
        return flask.redirect(redirect_url)

    return flask.redirect('/order')