# coding:utf8
"""

Author: ilcwd
"""

from .base import app as application


@application.route('/static/<name>')
def serve_static(name):
    return application.send_static_file(name)
