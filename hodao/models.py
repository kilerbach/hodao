# coding:utf8
"""
Created on 2014-9-2

@author: ilcwd
"""
import time
import datetime
import functools
from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, BIGINT, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Index

from hodao.core import C, spy_logger


Base = declarative_base()


class Order(Base):
    __tablename__ = 'order'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    user = Column(String(250), nullable=False)
    company = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    phone = Column(String(250), nullable=False)
    status = Column(Integer(), nullable=False)
    created_time = Column(DateTime(), nullable=False)
    modified_time = Column(DateTime(), nullable=False)


Index('_idx_order_user', Order.user)
Index('_idx_order_ctime', Order.created_time)


class OrderTrack(Base):
    __tablename__ = 'orderTrack'

    id = Column(Integer, primary_key=True)
    orderid = Column(Integer, nullable=False)
    operator = Column(String(250), nullable=False)
    note = Column(String(250), nullable=False)
    operated_time = Column(DateTime(), nullable=False)


Index('_idx_ordertrace_orderid', OrderTrack.orderid)


class Contact(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    phone = Column(BIGINT(), nullable=False)
    order = Column(Integer(), nullable=False)
    created_time = Column(DateTime(), nullable=False)
    modified_time = Column(DateTime(), nullable=False)
    is_deleted = Column(BOOLEAN(), nullable=False)

    def is_primary(self):
        return int(self.order) == ContactOrder.PRIMARY


Index('_idx_contact_user', Contact.user)


class Status(object):
    START_ = -1
    COLLECTED = 0
    TAKING = 1
    TAKEN = 2
    FINISH = 3
    EXPIRED = 4
    NOT_FOUND = 5
    END_ = 6


class ContactOrder(object):
    PRIMARY = 0
    OTHERS = 1


class UserRole(object):
    NOT_LOGIN = 0
    USER = 1
    ADMIN = 2


ORDER_STATUS_MAPPING = {
    Status.COLLECTED: u"已收录",
    Status.TAKING: u"取件中",
    Status.TAKEN: u"取件成功",
    Status.FINISH: u"已完成",
    Status.EXPIRED: u"已取消",
    Status.NOT_FOUND: u"未找到"
}

USER_ORDER_STATUS_MAPPING = ORDER_STATUS_MAPPING.copy().update({
    Status.NOT_FOUND: u"未能找到该快递"
})

ROLE_ALLOW_OPERATIONS = {
    # can change FROM status TO status.
    UserRole.USER: {
        Status.TAKEN: Status.FINISH,
        Status.COLLECTED: Status.EXPIRED,
    },

    UserRole.ADMIN: {
        Status.COLLECTED: None,
        Status.TAKING: None,
        Status.TAKEN: None,
    }
}


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine(C.DB_FILE, echo=C.DEBUG)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


@contextmanager
def create_session():
    session = DBSession()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def _log_costtime(func):
    name = __name__ + '.' + func.__name__

    @functools.wraps(func)
    def wrapper(*a, **kw):
        st = time.time()
        try:
            return func(*a, **kw)
        finally:
            ct = time.time() - st
            spy_logger.info("%s - %dms", name, int(ct))

    return wrapper


@_log_costtime
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


@_log_costtime
def query_orders(user):
    session = DBSession()
    return session.query(Order) \
        .filter(Order.user == user) \
        .order_by(Order.status, Order.created_time).all()


@_log_costtime
def query_all_orders():
    two_days_ago = datetime.date.today() - datetime.timedelta(days=4)
    session = DBSession()
    return session.query(Order) \
        .filter(Order.created_time > two_days_ago) \
        .order_by(Order.status, Order.created_time).all()


@_log_costtime
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
    if not (Status.START_ < int(status) <= Status.END_):
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


@_log_costtime
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


@_log_costtime
def query_contacts(user):
    session = DBSession()
    return session.query(Contact)\
        .filter(Contact.user == user)\
        .filter(Contact.is_deleted == False)\
        .all()


@_log_costtime
def delete_contact(user, contact_id):
    with create_session() as session:
        rows = session.query(Contact)\
            .filter(Contact.user == user)\
            .filter(Contact.id == contact_id).delete()
        return rows
