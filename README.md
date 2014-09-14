Ho道
====

Ho道网页和微信接口，见 [Ho道](http://www.ho-dao.com/)。

微信公众号搜索 **Ho道** 或者 **Ho-dao**。


Dependencies
----

    # running environment
    apt-get install nginx
    apt-get install uwsgi

    pip install fabric
    pip install virtualenv
    pip install nose

    # finally, install python 3rd party libraries.
    pip install -r requirements.txt


Test
----

    nosetest tests

Debug
----

    python wsgiapp.py

Deploy
----

    # init env, run once at first time.
    fab -f deployment/fabfile.py production init
    
    fab -f deployment/fabfile.py production deploy

Run
----

    ./runuwsgi.sh [start|stop|restart]
