# coding:utf8
"""

Author: ilcwd
"""
import traceback

from flask import render_template

from hodao.core import application


@application.errorhandler(500)
def error_handler(ex):
    print traceback.format_exc()
    return render_template('error.html', msg=u'服务器异常')


@application.errorhandler(400)
def handle_400(ex):
    return render_template('error.html', msg=u'参数错误')


@application.errorhandler(404)
def handle_404(ex):
    return render_template('error.html', msg=u'没有找到该网页')