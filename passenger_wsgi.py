# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/p/polivajh/prosvet/public_html')
sys.path.insert(1, '/home/p/polivajh/prosvet/public_html/venv/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'pro_core.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()