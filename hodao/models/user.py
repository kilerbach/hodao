# coding: utf8
#
# hoshop - user
# 
# Author: ilcwd 
# Create: 14/12/30
#
import datetime
import uuid

from hodao.core import C
from .base import User, Login, create_session, DBSession, log_costtime


class USER_TYPE:
    UNKNOWN = 0
    DEVICE = 1
    EMAIL = 2
    MOBILE = 3
    WECHAT = 4


class _BaseUser(object):
    def __init__(self):
        self.userid = None
        self.name = None
        self.type = None
        self.boundUsers = []  # of _BaseUser


class DeviceUser(_BaseUser):
    def __init__(self):
        super(DeviceUser, self).__init__()


def wechat_login(username):
    pass


@log_costtime
def device_login(deviceID):
    """
    Login with device unique ID.

    Attentions:

        * If deviceID is stolen by attackers, they can get all your info!

    Returns:

        Userinfo
    """
    with create_session() as session:
        logininfos = session.query(Login).filter(Login.loginid == deviceID)\
            .filter(Login.logintype == USER_TYPE.DEVICE).with_lockmode('update').all()
        if logininfos:
            logininfo = logininfos[0]
        else:
            now = datetime.datetime.now()
            userinfo = User(enable=True, created_time=now, modified_time=now)
            session.add(userinfo)
            logininfo = Login(userid=userinfo.userid, loginid=deviceID, logintype=USER_TYPE.DEVICE, password='',
                              enable=True, created_time=now, modified_time=now)
            session.add(logininfo)

        return logininfo


def main():
    import random


if __name__ == '__main__':
    main()