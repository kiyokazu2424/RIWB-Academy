"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# 本番環境
sys.path.append('/home/ec2-user/Django/riwb-academy')   #### 追加 ####
sys.path.append('/home/ec2-user/Django/riwb-academy/config/wsgi.py')   #### 追加 ####
# 本番環境ここまで
application = get_wsgi_application()
