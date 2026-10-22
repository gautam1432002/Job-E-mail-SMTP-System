"""
jobmailer/settings/prod.py
Production settings for Render.com deployment.
All secrets come from Render Environment Variables — never hardcoded.
"""
import dj_database_url
from .base import *  # noqa: F401, F403

DEBUG = False

# ─── Security hardening ───────────────────────────────────────────────────────
SECURE_PROXY_SSL_HEADER   = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT        = True
SESSION_COOKIE_SECURE      = True
CSRF_COOKIE_SECURE         = True
SECURE_HSTS_SECONDS        = 31536000   # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD        = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# ─── Database — PostgreSQL via DATABASE_URL env var ───────────────────────────
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', ''),
        conn_max_age=600,        # keep connections alive 10 min
        conn_health_checks=True,
    )
}

# ─── Logging (stdout → Render log stream) ─────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {'format': '[%(levelname)s] %(name)s: %(message)s'},
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {'handlers': ['console'], 'level': 'INFO'},
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'WARNING', 'propagate': False},
        'mailer': {'handlers': ['console'], 'level': 'INFO',    'propagate': False},
    },
}
