# coding:utf8
"""

Author: ilcwd
"""
import datetime

from .base import (
    log_costtime,
    create_session,
    DBSession,
    Contact,
    ContactOrder,
)


@log_costtime
def create_contact(user, name, phone):
    now = datetime.datetime.now()

    with create_session() as session:
        rows = session.query(Contact).filter(Contact.user == user).with_lockmode('update').all()

        has_primary = False
        for c in rows:
            if c.is_primary():
                has_primary = True

            if c.name == name and str(c.phone) == str(phone):
                return 0

        contact = Contact(user=user, name=name, phone=phone,
                          order=ContactOrder.OTHERS,
                          created_time=now, modified_time=now,
                          is_deleted=False)
        # if no primary, set it to primary
        if not has_primary:
            contact.order = ContactOrder.PRIMARY

        session.add(contact)

    return 1


@log_costtime
def query_contacts(user):
    session = DBSession()
    return session.query(Contact)\
        .filter(Contact.user == user)\
        .filter(Contact.is_deleted == False)\
        .all()


@log_costtime
def delete_contact(user, contact_id):
    with create_session() as session:
        rows = session.query(Contact)\
            .filter(Contact.user == user)\
            .filter(Contact.id == contact_id).delete()
        return rows


@log_costtime
def set_contact_primary(user, contact_id):
    now = datetime.datetime.now()
    with create_session() as session:
        rows = session.query(Contact).filter(Contact.user == user).with_lockmode('update').all()
        if not rows:
            return 0

        for c in rows:
            if int(c.id) == int(contact_id) and c.order == ContactOrder.PRIMARY:
                return 1

        update_params = {'order': ContactOrder.OTHERS, 'modified_time': now}
        session.query(Contact).\
            filter(Contact.user == user and Contact.order == ContactOrder.PRIMARY).\
            update(update_params)

        update_params['order'] = ContactOrder.PRIMARY
        session.query(Contact).\
            filter(Contact.user == user and Contact.id == contact_id).\
            update(update_params)

    return 1