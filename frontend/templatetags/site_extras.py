from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from django.utils.html import strip_tags

from frontend.models import SiteContent
from staff_portal.rich_text import sanitize_html

register = template.Library()


def _current_lang():
    lang = (get_language() or 'en')[:2]
    return lang if lang in ('en', 'es') else 'en'


def _resolve_content(key, default=''):
    lang = _current_lang()
    text = SiteContent.get_text(key, language=lang, default='')
    return text or default


def _wrap_editable(context, key, inner_html, *, content_format='html'):
    if not context.get('content_edit_mode'):
        return inner_html
    label = escape(key.replace('-', ' '))
    return mark_safe(
        f'<span class="staff-editable" data-content-key="{escape(key)}" '
        f'data-content-format="{escape(content_format)}" tabindex="0" role="button" '
        f'aria-label="Edit {label}">{inner_html}</span>'
    )


@register.simple_tag(takes_context=True)
def site_content(context, key, default=''):
    """Plain text only — strips any formatting."""
    text = strip_tags(_resolve_content(key, default))
    if context.get('content_edit_mode'):
        return _wrap_editable(
            context,
            key,
            escape(text) if text else mark_safe('<span class="staff-editable-empty">Click to add text</span>'),
            content_format='plain',
        )
    return text


@register.simple_tag(takes_context=True)
def site_content_html(context, key, default=''):
    """Safe HTML for paragraphs, bold text, and lists."""
    html = mark_safe(sanitize_html(_resolve_content(key, default)))
    if context.get('content_edit_mode'):
        if not strip_tags(str(html)).strip():
            html = mark_safe('<span class="staff-editable-empty">Click to add text</span>')
        return _wrap_editable(context, key, html, content_format='html')
    return html


@register.simple_tag(takes_context=True)
def site_text(context, key, default=''):
    """Short plain-text label (navigation, headings, buttons)."""
    text = strip_tags(_resolve_content(key, default))
    if context.get('content_edit_mode'):
        return _wrap_editable(
            context,
            key,
            escape(text) if text else mark_safe('<span class="staff-editable-empty">Click to add text</span>'),
            content_format='plain',
        )
    return text


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
