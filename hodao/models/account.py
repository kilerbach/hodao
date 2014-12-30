# coding: utf8
#
# hoshop - user
# 
# Author: ilcwd 
# Create: 14/12/30
#


class USER_TYPE:
    WECHAT = 0
    IOS_DEVICE = 1
    EMAIL = 2
    MOBILE = 3


class _BaseUser(object):
    def __init__(self):
        self.userid = None
        self.name = None
        self.type = None
        self.boundUsers = []  # of _BaseUser


def login():
    pass


def main():
    pass


if __name__ == '__main__':
    main()