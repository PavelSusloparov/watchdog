import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('home/acekool/.virtualenvs/watchdog/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
#sys.path.insert(0, '/home/acekool/.virtualenvs/watchdog/')
sys.path.insert(0, '/home/acekool/.virtualenvs/watchdog/testRunService')
sys.path.insert(0, '/home/acekool/.virtualenvs/watchdog/testRunService/testRunService')
sys.path.insert(0, '/home/acekool/.virtualenvs/watchdog/testRunService/trs')

os.environ['DJANGO_SETTINGS_MODULE'] = 'testRunService.settings'

# Activate your virtual env
#activate_env=os.path.expanduser("~/.virtualenvs/watchdog/bin/activate_this.py")
#execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
