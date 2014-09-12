# coding:utf8
"""

Author: ilcwd
"""

from base import *


def test_web_ui():
    assert u"Ho单列表" in web_rpc('/order')

    assert u"已仔细阅读代取事项" in web_rpc('/order/create')

    assert u"需要管理员权限" in web_rpc('/order/manage')

    assert u"没有找到该网页" in web_rpc('/404notfound')


def main():
    test_web_ui()

    print "fin"


if __name__ == '__main__':
    main()
