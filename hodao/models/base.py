# coding:utf8
"""

Author: ilcwd
"""
import time
import functools
from contextlib import contextmanager
import inspect

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, BIGINT, BOOLEAN, VARBINARY
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


class User(Base):
    __tablename__ = 'user'
    userid = Column(Integer, primary_key=True, autoincrement=True)

    created_time = Column(DateTime(), nullable=False)
    modified_time = Column(DateTime(), nullable=False)
    enable = Column(BOOLEAN, nullable=False)


class Login(Base):
    __tablename__ = 'login'
    autoid = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, nullable=False)

    loginid = Column(String(250), nullable=False)
    logintype = Column(Integer, nullable=False)
    password = Column(VARBINARY(250), nullable=False)

    created_time = Column(DateTime(), nullable=False)
    modified_time = Column(DateTime(), nullable=False)
    enable = Column(BOOLEAN, nullable=False)


Index('_idx_login_userid', Login.userid)
Index('_uidx_login_logintype_loginid', Login.logintype, Login.loginid, unique=True)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine(C.DB_FILE, echo=C.DEBUG)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


class OrderStatus(object):
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
    OrderStatus.COLLECTED: u"已收录",
    OrderStatus.TAKING: u"取件中",
    OrderStatus.TAKEN: u"取件成功",
    OrderStatus.FINISH: u"已完成",
    OrderStatus.EXPIRED: u"已取消",
    OrderStatus.NOT_FOUND: u"未找到"
}

USER_ORDER_STATUS_MAPPING = ORDER_STATUS_MAPPING.copy().update({
    OrderStatus.NOT_FOUND: u"未能找到该快递"
})

ROLE_ALLOW_OPERATIONS = {
    # can change FROM status TO status.
    UserRole.USER: {
        OrderStatus.TAKEN: OrderStatus.FINISH,
        OrderStatus.COLLECTED: OrderStatus.EXPIRED,
    },

    UserRole.ADMIN: {
        OrderStatus.COLLECTED: None,
        OrderStatus.TAKING: None,
        OrderStatus.TAKEN: None,
    }
}


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


def log_costtime(func):
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    funcname = mod.__name__ + '.' + func.__name__

    @functools.wraps(func)
    def wrapper(*a, **kw):
        st = time.time()
        try:
            return func(*a, **kw)
        finally:
            ct = time.time() - st
            spy_logger.info("%s - %dms", funcname, int(ct))

    return wrapper
