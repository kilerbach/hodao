# coding:utf8
"""

Author: ilcwd
"""

from collections import defaultdict

import flask
from flask import render_template, request

from hodao.core import application, C
from hodao import models, util


def _render_login_page():
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


@application.route('/static/<name>')
def serve_static(name):
    return application.send_static_file(name)


@application.route('/')
def index():
    user = flask.session.get('user')
    contacts = models.query_contacts(user)
    return render_template('index.html', contacts=contacts)


@application.route('/contact')
def query_contact():
    user = flask.session.get('user')
    if not user:
        return _render_login_page()

    contacts = models.query_contacts(user)
    return render_template('contacts.html', contacts=contacts)


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

    def _get_date(dt):
        return dt.strftime("%Y-%m-%d")

    for o in orders:
        date = _get_date(o.created_time)
        date_express_orders[date][o.company].append(o)

    result = []
    for d, ex_ords in sorted(date_express_orders.items(), reverse=True):
        for ex, ods in sorted(ex_ords.items()):
            result.append([(d, ex), sorted(ods, key=lambda x: x.created_time, reverse=True)])

    return render_template(
        'management.html',
        sorted_orders=result,
        order_status_mapping=models.ORDER_STATUS_MAPPING,
    )


@application.route('/order/create', methods=['GET', 'POST'])
def create_order():
    if request.method == 'GET':
        return render_template('index.html')

    phone = request.form['phone']
    company = request.form['company']
    name = request.form['name']
    amount = int(request.form.get('amount', 1))
    save_contact = request.form.get('savecontact', 'off') == 'on'

    user = flask.session.get('user')
    if user:
        models.create_order(user, name, company, phone, amount)
    else:
        return _render_login_page()

    if save_contact:
        models.create_contact(user, name, phone)

    return flask.redirect('/order')


@application.route('/order/update', methods=['POST'])
def update_order():
    order_id = request.form['order_id']
    status = request.form['status']

    # check permission
    user = flask.session.get('user')
    if not (user or flask.session.get('admin')):
        return _render_login_page()

    models.update_order(order_id, int(status), user or None)
    redirect_url = request.form.get('next')
    if redirect_url:
        return flask.redirect(redirect_url)

    return flask.redirect('/order')


@application.route('/login', methods=['GET', 'POST'])
def login():
    u = request.values.get('u')
    t = request.values.get('t')
    s = request.values.get('s')
    redirect_url = request.values.get('next')

    if not (u and t and s) or not util.valid_request(s, u, t):
        return _render_login_page()

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
