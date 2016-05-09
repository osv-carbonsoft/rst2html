#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import shutil
## sys.stdout = sys.stderr
import cgitb
cgitb.enable()
import cherrypy

ROOT = os.path.dirname(os.path.abspath(__file__)) # '/home/albert/rst2html'
os.chdir(ROOT)
sys.path.insert(0, ROOT)
shutil.copyfile('app_settings_mongo.py', 'app_settings.py')
from rst2html import Rst2Html

application = cherrypy.tree.mount(Rst2Html())
cherrypy.config.update({'environment': 'embedded'})
cherrypy.config.update({'engine.autoreload_on': False,
        })
