# coding:utf8
"""

Author: ilcwd
"""

from hodao.core import application


@application.route('/static/<name>')
def serve_static(name):
    return application.send_static_file(name)
