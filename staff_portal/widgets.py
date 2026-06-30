from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from staff_portal.rich_text import prepare_html_for_editor


class RichTextWidget(forms.Widget):
    """Visual text editor — no HTML tags shown to staff."""

    template_name = 'staff_portal/widgets/rich_text.html'

    def __init__(self, attrs=None):
        default_attrs = {'class': 'staff-rich-text-source d-none'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    class Media:
        css = {
            'all': (
                'https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.snow.css',
                'css/staff_rich_text.css',
            ),
        }
        js = (
            'https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.js',
            'js/staff_rich_text.js',
        )

    def format_value(self, value):
        if value is None:
            return ''
        return prepare_html_for_editor(str(value))

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(render_to_string(self.template_name, context))
