"""
jobmailer/settings/__init__.py
Auto-routes to the correct environment settings.
DJANGO_SETTINGS_MODULE=jobmailer.settings  → picks dev or prod based on DJANGO_ENV
DJANGO_SETTINGS_MODULE=jobmailer.settings.prod  → directly loads prod (Render)
"""
import os

_env = os.getenv('DJANGO_ENV', 'dev')

if _env == 'prod':
    from .prod import *   # noqa: F401, F403
else:
    from .dev import *    # noqa: F401, F403
