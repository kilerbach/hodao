# coding:utf8
"""

Author: ilcwd
"""
import flask
from flask import render_template
# noinspection PyUnresolvedReferences
from flask.ext.paginate import Pagination

from hodao.core import application
from hodao.models import contact
from hodao.views.user import render_login_page


@application.route('/contact')
def query_contact():
    user = flask.session.get('user')
    if not user:
        return render_login_page()

    contacts = contact.query_contacts(user)
    return render_template('contacts.html', contacts=contacts)
