"""Sanitize and normalize HTML for the staff rich-text editor."""

import re

import bleach

ALLOWED_TAGS = ['p', 'br', 'strong', 'b', 'em', 'i', 'u', 'ul', 'ol', 'li']
ALLOWED_ATTRIBUTES = {}


def prepare_html_for_editor(html: str) -> str:
    """Convert legacy markup (e.g. styled spans) into editor-friendly HTML."""
    if not html:
        return ''
    text = html.strip()
    # Legacy bootstrap content used colored spans — show as bold in the editor.
    text = re.sub(
        r'<span[^>]*class="[^"]*fw-bold[^"]*"[^>]*>(.*?)</span>',
        r'<strong>\1</strong>',
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(
        r'<span[^>]*class="[^"]*text-love[^"]*"[^>]*>(.*?)</span>',
        r'<strong>\1</strong>',
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(
        r'<span[^>]*class="[^"]*text-primary[^"]*"[^>]*>(.*?)</span>',
        r'<strong>\1</strong>',
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(r'<br\s*/?>', '<br>', text, flags=re.IGNORECASE)
    return text


def sanitize_html(html: str) -> str:
    """Strip unsafe tags; keep only simple formatting staff can create in the editor."""
    if not html:
        return ''
    cleaned = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
    )
    cleaned = re.sub(r'(\s*<br\s*/?>\s*){3,}', '<br><br>', cleaned, flags=re.IGNORECASE)
    return cleaned.strip()
