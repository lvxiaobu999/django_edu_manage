"""
ASGI config for django_edu_manage project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

django_env = os.environ.get('DJANGO_ENV', 'development').strip().lower() or 'development'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'django_edu_manage.settings.{django_env}')

application = get_asgi_application()
