#coding:utf8
"""
Created on 2014-9-2

@author: ilcwd
"""

import sys
reload(sys).setdefaultencoding('utf8')
import logging.config
import os

import yaml

# load logging configs
DEPLOYMENT_DIR = os.path.join(os.path.dirname(__file__), 'deployment')
logging_config_path = os.path.join(DEPLOYMENT_DIR, 'logging.yaml')
with open(logging_config_path, 'r') as f:
    logging.config.dictConfig(yaml.load(f))

from hodao.core import application, C

# load application configs, MUST be run before import views and models!
C.load_config(os.path.join(DEPLOYMENT_DIR, 'config.json'))

application.secret_key = C.SERVER_SESSION_KEY
application.debug = C.DEBUG

# register views
from hodao.views import *


def main():
    host, port = '0.0.0.0', 8080
    debug = C.DEBUG

    application.run(host, port, debug, use_reloader=False)
    
if __name__ == '__main__':
    main()