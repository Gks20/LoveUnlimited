from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from django.utils.html import strip_tags

from frontend.models import SiteContent
from staff_portal.rich_text import sanitize_html

register = template.Library()


def _resolve_content(key, default=''):
    lang = (get_language() or 'en')[:2]
    if lang not in ('en', 'es'):
        lang = 'en'
    text = SiteContent.get_text(key, language=lang, default='')
    return text or default


@register.simple_tag
def site_content(key, default=''):
    """Plain text only — strips any formatting."""
    return strip_tags(_resolve_content(key, default))


@register.simple_tag
def site_content_html(key, default=''):
    """Safe HTML for paragraphs, bold text, and lists."""
    return mark_safe(sanitize_html(_resolve_content(key, default)))


@register.filter
def person_initials(name):
    """First + last initial for avatar placeholders."""
    parts = (name or '').strip().split()
    if len(parts) >= 2:
        return f'{parts[0][0]}{parts[-1][0]}'.upper()
    if parts:
        return parts[0][:2].upper()
    return '?'


@register.filter
def post_body_html(value):
    """Render post body as safe HTML (rich text or legacy plain text)."""
    if not value:
        return ''
    text = value.strip()
    if '<' in text and '>' in text:
        return mark_safe(sanitize_html(text))
    paragraphs = [f'<p>{escape(p.strip())}</p>' for p in text.split('\n\n') if p.strip()]
    if paragraphs:
        return mark_safe(''.join(paragraphs))
    return mark_safe(f'<p>{escape(text)}</p>')