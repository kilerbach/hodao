# coding:utf8
"""

Author: ilcwd
"""

from collections import defaultdict

import flask
from flask import render_template, request

from hodao.core import application, C
from hodao import models, util


@application.route('/static/<name>')
def serve_static(name):
    return application.send_static_file(name)


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/order')
def show_orders():
    user = flask.session.get('user')
    if user:
        if flask.session.get('admin'):
            orders = models.query_all_orders()
        else:
            orders = models.query_orders(user)
    else:
        orders = []
    return render_template('orders.html', orders=orders)


@application.route('/order/manage')
def manage_orders():
    if not flask.session.get('admin'):
        return render_template('error.html', msg=u"需要管理员权限")

    orders = models.query_all_orders()
    date_express_orders = defaultdict(lambda: defaultdict(list))
    date_count = defaultdict(int)

    def _get_date(dt):
        return dt.strftime("%Y-%m-%d")

    for o in orders:
        date = _get_date(o.created_time)
        date_express_orders[date][o.company].append(o)
        date_count[date] += 1

    orders = sorted(orders, key=lambda x: (_get_date(x.created_time), x.company), reverse=True)
    pre_date = None
    pre_company = None
    date_split = []
    company_split = []
    for ix, o in enumerate(orders):
        date = _get_date(o.created_time)
        date_changed = False
        if pre_date != date:
            date_split.append(date_count[date])
            pre_date = date
            date_changed = True
        else:
            date_split.append(0)

        if pre_company != o.company or date_changed:
            company_split.append(len(date_express_orders[date][o.company]))
            pre_company = o.company
        else:
            company_split.append(0)

    return render_template('management.html',
                           sorted_orders=orders, date_split=date_split, company_split=company_split)


@application.route('/order/update', methods=['POST'])
def update_order():
    order_id = request.form['order_id']
    status = request.form['status']
    models.update_orders(order_id, int(status))
    redirect_url = request.form.get('next')
    if redirect_url:
        return flask.redirect(redirect_url)

    return flask.redirect('/order')


@application.route('/order/create', methods=['GET', 'POST'])
def create_order():
    if request.method == 'GET':
        return render_template('index.html')

    phone = request.form['phone']
    company = request.form['company']
    name = request.form['name']

    user = flask.session.get('user')
    if user:
        models.create_order(user, name, company, phone)
    else:
        return render_template('error.html', msg=u"请先登录")

    return flask.redirect('/order')


@application.route('/login', methods=['GET', 'POST'])
def login():
    u = request.values.get('u')
    t = request.values.get('t')
    s = request.values.get('s')
    redirect_url = request.values.get('next')

    if not (u and t and s) or not util.valid_request(s, u, t):
        return render_template('error.html', msg=u"请先登录")

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
