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

