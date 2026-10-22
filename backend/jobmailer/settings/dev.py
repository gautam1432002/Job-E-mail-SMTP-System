"""
jobmailer/settings/dev.py
Local development settings — uses SQLite, shows full errors.
"""
from .base import *  # noqa: F401, F403

DEBUG = True

# SQLite is fine locally
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Serve media files directly in dev
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Allow the django-debug-toolbar if installed
INTERNAL_IPS = ['127.0.0.1']
