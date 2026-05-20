import os


DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development').strip().lower() or 'development'

if DJANGO_ENV == 'production':
    from .production import *
else:
    from .development import *
