"""
WSGI config for django_edu_manage project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

django_env = os.environ.get('DJANGO_ENV', 'development').strip().lower() or 'development'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'django_edu_manage.settings.{django_env}')

application = get_wsgi_application()
