"""
jobmailer/settings.py  ← LEGACY REDIRECT FILE
This file now simply re-exports from the split settings package.
Delete this file once you're fully migrated.
"""
import os

env = os.getenv('DJANGO_ENV', 'dev')
if env == 'prod':
    from .settings.prod import *   # noqa
else:
    from .settings.dev import *    # noqa
