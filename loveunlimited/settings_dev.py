"""Development settings profile."""
from decouple import config
from .settings_base import *  # noqa: F401,F403

SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-key-in-production')
DEBUG = True
# Allow common local hosts and strip whitespace to avoid mismatches
_hosts_raw = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,192.168.1.81,192.168.1.64')
ALLOWED_HOSTS = [h.strip() for h in _hosts_raw.split(',') if h.strip()]

# Dev: print emails to console; no real sending.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Extra dev tools placeholder (e.g., django-debug-toolbar) can be added here.
