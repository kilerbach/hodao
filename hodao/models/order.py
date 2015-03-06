# coding:utf8
"""

Author: ilcwd
"""
import datetime

from hodao.core import C
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

    created_time = datetime.datetime.now()
    if C.NEXT_DAY_ORDER_START_HOUR <= created_time.hour < C.NEXT_DAY_ORDER_END_HOUR:
        next_day = created_time + datetime.timedelta(days=1)
        created_time = datetime.datetime(next_day.year, next_day.month, next_day.day)

    with create_session() as session:
        for i in xrange(amount):
            new_order = Order(user=user, name=name, company=company, phone=phone, status=0,
                              created_time=created_time, modified_time=created_time)
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

    today = datetime.date.today()

    # two days one page.
    paging_step = 2

    # if today is 2014-10-15, date of end is 2014-10-14,
    # so need to 1 day ahead.
    end = today - datetime.timedelta(days=paging_step*pagination - 1)
    start = end + datetime.timedelta(days=paging_step)

    session = DBSession()
    last_record = session.query(Order).order_by(Order.created_time).limit(1).one()

    # ext.paginate use `total` to calculate how many pages,
    # so we provide a dummy one
    total = (today - last_record.created_time.date()).days / paging_step * page_size + 1

    if pagination == 1:
        query = session.query(Order).filter(Order.created_time >= end)
    else:
        query = session.query(Order).filter(Order.created_time < start)\
            .filter(Order.created_time >= end)
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