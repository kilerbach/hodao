# coding:utf8
"""

Author: ilcwd
"""

import flask
from flask import jsonify, request

from hodao.core import application
from hodao import models


@application.route('/ajax/order')
def ajax_orders():
    if not flask.session.get('admin'):
        return jsonify({"status": 1, "error": u"需要管理员权限"})

    return jsonify({"status": 0, "error": u"成功"})


@application.route('/ajax/order/update', methods=["POST"])
def ajax_update_order():
    # check permission
    user = flask.session.get('user') or None
    if not (user or flask.session.get('admin')):
        return jsonify({"status": 1, "error": u"需要登录"})

    order_id = request.form['order_id']
    status = request.form['status']
    rows = models.update_order(order_id, status, user)

    if rows > 0:
        return jsonify({"status": 0, "error": u"成功"})
    else:
        return jsonify({"status": 1, "error": u"更新失败"})


@application.route('/ajax/contact/create', methods=["POST"])
def ajax_create_contact():
    user = flask.session.get('user')
    if not user:
        return jsonify({"status": 1, "error": u"需要登录"})

    name = request.form['name']
    phone = request.form['phone']
    rows = models.create_contact(user, name, phone)
    if rows > 0:
        return jsonify({"status": 0, "error": u"成功"})
    else:
        return jsonify({"status": 1, "error": u"添加失败"})


@application.route('/ajax/contact/delete', methods=["POST"])
def ajax_delete_contact():
    user = flask.session.get('user')
    if not user:
        return jsonify({"status": 1, "error": u"需要登录"})

    contact_id = request.form['contact_id']
    rows = models.delete_contact(user, contact_id)
    if rows > 0:
        return jsonify({"status": 0, "error": u"成功"})
    else:
        return jsonify({"status": 1, "error": u"删除失败"})