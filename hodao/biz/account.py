# coding: utf8
#
# hoshop - account
# 
# Author: ilcwd 
# Create: 15/1/30
#

from hodao.models import user, session


def device_login(deviceid):
    u = user.device_login(deviceid)
    if not user:
        # TODO:
        return None, None

    userinfo = {
        'userid': u.userid,
        'loginid': u.loginid,
        'logintype': u.logintype,
    }

    token = session.create_session(userinfo, session.SESSION_TYPE.DEVICE)

    result = {
        'token': token,
    }
    result.update(userinfo)
    return result



def main():
    pass


if __name__ == '__main__':
    main()