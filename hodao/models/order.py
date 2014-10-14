# coding:utf8
"""

Author: ilcwd
"""
import datetime

from .base import (
    log_costtime,
    create_session,
    Order,
    OrderStatus,
    DBSession,
)


@log_costtime
def create_order(user, name, company, phone, amount):
    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()
    with create_session() as session:
        for i in xrange(amount):
            new_order = Order(user=user, name=name, company=company, phone=phone, status=0,
                              created_time=datetime.datetime.now(), modified_time=datetime.datetime.now())
            session.add(new_order)


@log_costtime
def query_orders(user):
    session = DBSession()
    return session.query(Order) \
        .filter(Order.user == user) \
        .order_by(Order.status, Order.created_time).all()


@log_costtime
def query_all_orders(pagination=1, page_size=5):
    if pagination < 1:
        return []

    session = DBSession()
    total = session.query(Order).count()
    query = session.query(Order).order_by(Order.created_time.desc())\
        .offset((pagination-1)*page_size)\
        .limit(page_size)
    return total, query.all()


@log_costtime
def update_order(order_id, status, user=None):
    """
    :param order_id:
    :param status:
    :param user:
    :return:
        -1 - error
        0 - order not found
        1 - success
    """
    # TODO:
    if not (OrderStatus.START_ < int(status) <= OrderStatus.END_):
        return -1

    now = datetime.datetime.now()
    update_params = {'status': status, 'modified_time': now}
    with create_session() as session:
        if user:
            rows = session.query(Order) \
                .filter(Order.id == order_id) \
                .filter(Order.user == user) \
                .update(update_params)
        else:
            rows = session.query(Order) \
                .filter(Order.id == order_id) \
                .update(update_params)
        return rows