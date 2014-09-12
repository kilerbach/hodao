# coding:utf8
"""

Author: ilcwd
"""
import traceback
import logging
import uuid

from flask import render_template, session, request

from hodao.core import application, C


_logger = logging.getLogger(__name__)


@application.errorhandler(500)
def error_handler(ex):
    _logger.error("Exception <%s>, Traceback: %s", str(ex), traceback.format_exc())
    return render_template('error.html', msg=u'服务器异常')


@application.errorhandler(400)
def handle_400(ex):
    return render_template('error.html', msg=u'参数错误')


@application.errorhandler(404)
def handle_404(ex):
    return render_template('error.html', msg=u'没有找到该网页')


@application.before_request
def csrf_protect():

    # exceptions ~
    if request.path == C.WECHAT_API:
        return

    if request.method == "POST":
        session_token = session.get('_csrf_token')
        form_token = request.form.get('_csrf_token')

        if not session_token or session_token != form_token:
            return render_template('error.html', msg=u'跨站错误')


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = uuid.uuid4().hex
    return session['_csrf_token']


application.jinja_env.globals['csrf_token'] = generate_csrf_token