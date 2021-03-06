"""Not the current startup file, not currently maintained
"""
import sys
sys.stdout = sys.stderr
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent)

import atexit
import threading
import cherrypy
from rst2html import Rst2Html

cherrypy.config.update({'environment': 'embedded'})

if cherrypy.__version__.startswith('3.0') and cherrypy.engine.state == 0:
    cherrypy.engine.start(blocking=False)
    atexit.register(cherrypy.engine.stop)

application = cherrypy.Application(Rst2Html(), script_name=None, config=None)
