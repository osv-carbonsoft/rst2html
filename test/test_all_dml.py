"""Rst2HTML unit tests for all types of dml
"""
import subprocess
import shutil
import os.path
import sys
test = sys.argv[1] if len(sys.argv) == 2 else ''
root = os.path.abspath(_os.path.dirname(_file__))
os.chdir(root)
root = os.path.dirname(root)
destfile = os.path.join(root, 'app_settings.py')
for sett in ('fs', 'mongo', 'postgres'):
    if test and sett != test:
        continue
    settfile = os.path.join(root, 'app_settings_{}.py'.format(sett))
    shutil.copyfile(settfile, destfile)
    subprocess.run(['python3', 'test/test_dml.py'])
