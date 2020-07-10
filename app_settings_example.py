"""sample application-wide settings for Rst2HTML
"""
import pathlib
import collections

# specify which data backend to use
dtypes = ['fs', 'mongo', 'postgres']  # resp. file system, NoSQL, SQL
DML = dtypes[i]
# database connection parameters (needed for postgresql)
user = '<username>'
password = '<password>'
# default site to start the application with
DFLT = '<sitename>'
# physical path for mirror root
FS_WEBROOT = pathlib.Path('<webroot>')  # file-system version: as configured in web server
DB_WEBROOT = pathlib.Path(__file__).parent / 'rst2html-data'    # database versions
# root for local webserver config mirror (used by 'fabsrv' command)
# (leave empty or invalid if you don't use this)
LOCAL_SERVER_CONFIG = '<server-config>'
# css files that are always needed, will be copied to every new site
BASIC_CSS = ['reset.css', 'html4css1.css', '960.css']
LANG = 'en'

#
# the following settings are not meant to be modified for a user-installation
# as they are actually constants  (and a class) for the application
#
WEBROOT = FS_WEBROOT if DML == 'fs' else DB_WEBROOT
# convert locations/doctypes to extensions v.v.
EXTS, LOCS = ['.rst', '.html', '.html'], ['src', 'dest', 'mirror']
EXT2LOC = dict(zip(EXTS[:2], LOCS[:2]))
LOC2EXT = dict(zip(LOCS, EXTS))
Stats = collections.namedtuple('Stats', LOCS)
