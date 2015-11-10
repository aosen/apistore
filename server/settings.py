# -*- coding: utf-8 -*-
import os.path
import socket
import logging
import sys

sys.path.append('../../')
from conf import *

logger = logging.getLogger('apistore')

DATABASES = DATABASES["default"]
