"""Resolve UI strings from SiteContent for the active language."""

from django.utils.translation import get_language

from frontend.models import SiteContent


def current_language():
    lang = (get_language() or 'en')[:2]
    return lang if lang in ('en', 'es') else 'en'


def localized_text(key, default=''):
    text = SiteContent.get_text(key, language=current_language(), default=default)
    return text or default
