# coding:utf8
"""

Author: ilcwd
"""
import traceback
import logging
import uuid

from flask import render_template, session, request, blueprints

from hodao.core import application, C
from hodao.util import NeedLoginException, NeedSuperException

_logger = logging.getLogger(__name__)


app = blueprints.Blueprint('web', __name__)


@app.errorhandler(NeedLoginException)
def handle_need_login(ex):
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
    ), 401


@app.errorhandler(NeedSuperException)
def handle_400(ex):
    return render_template('error.html', msg=u'需要管理员权限'), 401


# @app.errorhandler(500)
# def error_handler(ex):
#     _logger.error("Exception <%s>, Traceback: %s", str(ex), traceback.format_exc())
#     return render_template('error.html', msg=u'服务器异常'), 500


@app.errorhandler(400)
def handle_400(ex):
    return render_template('error.html', msg=u'参数错误'), 400


@app.errorhandler(404)
def handle_404(ex):
    return render_template('error.html', msg=u'没有找到该网页'), 404


@app.before_request
def csrf_protect():

    # exceptions ~
    if request.path.startswith((C.WECHAT_API, '/api')):
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