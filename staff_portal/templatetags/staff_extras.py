from django import template

from staff_portal.content_labels import CONTENT_LABELS, CONTENT_SECTIONS, SECTION_BY_KEY

register = template.Library()


@register.filter
def content_label(key):
    return CONTENT_LABELS.get(key, key.replace('-', ' ').title())


@register.filter
def content_section_title(key):
    section_id = SECTION_BY_KEY.get(key)
    if not section_id:
        return 'Other'
    for sid, title, _help, _items in CONTENT_SECTIONS:
        if sid == section_id:
            return title
    return 'Other'
