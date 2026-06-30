"""
Environment-aware settings loader.

Delegates to environment-specific modules built on top of a common
base configuration. Use DJANGO_ENV=dev|prod|test to select the profile.
"""
from decouple import config

ENV = config('DJANGO_ENV', default='dev').lower()

if ENV == 'prod':
    from .settings_prod import *  # noqa: F401,F403
elif ENV == 'test':
    from .settings_dev import *  # reuse dev base for tests
else:
    from .settings_dev import *  # noqa: F401,F403

PRINT_ENV = config('PRINT_SETTINGS_ENV', default=False, cast=bool)
if PRINT_ENV:
    import sys
    print(f"[settings] Loaded environment profile: {ENV}", file=sys.stderr)
