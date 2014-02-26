#!../venv/bin/python
# encoding: utf-8

import sys
import os

sys.dont_write_bytecode = True
sys.path.append("../../venv/local/lib/python2.7/site-packages")
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from wsgiref.handlers import CGIHandler
from sanotut import app
from werkzeug.debug import DebuggedApplication
from werkzeug.contrib.fixers import ProxyFix

if 'PATH_INFO' not in os.environ :
        os.environ['PATH_INFO'] = ''

app = ProxyFix(app)
app = DebuggedApplication(app, evalex=True)
app.debug = True

CGIHandler().run(app)
