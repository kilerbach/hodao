# coding:utf8
"""

Author: ilcwd
"""

import flask
from flask import render_template, jsonify

from hodao.core import application


@application.route('/ajax/order')
def orders():
    if not flask.session.get('admin'):
        return jsonify({"status": 1, "error": u"需要管理员权限"})

    return jsonify({"status": 0, "error": u"成功"})
