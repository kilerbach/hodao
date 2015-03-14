# coding: utf8
#
# hoshop - counter
# 
# Author: ilcwd 
# Create: 15/3/11
#

import datetime

from .base import get_redis
from hodao.core import C


REDIS_KEY_EXPRESS_DAILY_QUOTA_KEY = 'EXPRESS:DAILY:QUOTA:'


def _todays_quota_key():
    created_time = datetime.datetime.now()
    if C.NEXT_DAY_ORDER_START_HOUR <= created_time.hour < C.NEXT_DAY_ORDER_END_HOUR:
        created_time = created_time + datetime.timedelta(days=1)

    postfix = created_time.strftime("%Y%m%d")
    return REDIS_KEY_EXPRESS_DAILY_QUOTA_KEY + postfix


def query_left_express_daily_quota():
    todays_quota_key = _todays_quota_key()
    db = get_redis()
    quota = db.get(todays_quota_key)
    if quota is None:
        db.setnx(todays_quota_key, C.EXPRESS_DAILY_QUOTA)

        quota = db.get(todays_quota_key)

    if quota < 0:
        quota = 0

    return int(quota)


def minus_express_daily_quota(n=1):
    db = get_redis()
    todays_quota_key = _todays_quota_key()

    query_left_express_daily_quota()

    return db.decr(todays_quota_key, n)