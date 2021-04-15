"""
WSGI config for firesmokedetector project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os,sys

sys.path.append('/home/prathamesh/Fire-Smoke-Detection-WebApp')

sys.path.append('/home/prathamesh/Fire-Smoke-Detection-WebApp/env2/lib/python3.6/site-packages')


python_home = '/home/prathamesh/Fire-Smoke-Detection-WebApp/env'

activate_this = python_home + '/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))

#with open(activate_this) as f:
 #   exec(f.read(), {'__file__': activate_this})

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firesmokedetector.settings')

application = get_wsgi_application()
