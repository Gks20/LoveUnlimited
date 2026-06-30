from django import forms
from django.utils.html import strip_tags
from django.utils.text import slugify

from calendar_app.models import Event, EventCategory
from frontend.models import (
    Post, SiteContent, TeamMember, Resource, ResourceCategory, DonationSettings,
)
from staff_portal.content_format import PLAIN_TEXT_KEYS, SINGLE_LINE_KEYS
from staff_portal.rich_text import sanitize_html
from staff_portal.widgets import RichTextWidget


class StyledForm(forms.ModelForm):
    """Bootstrap form with larger, easier-to-use controls."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = 'form-control form-control-lg'
            if isinstance(field.widget, forms.CheckboxInput):
                css = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                css = 'form-select form-select-lg'
            elif isinstance(field.widget, forms.Textarea):
                css = 'form-control form-control-lg'
                field.widget.attrs.setdefault('rows', 5)
            field.widget.attrs.setdefault('class', css)


class EventForm(StyledForm):
    field_groups = [
        (
            'What is this event?',
            'Give it a name and describe what people can expect.',
            ['title', 'description', 'category'],
        ),
        (
            'When and where?',
            'Pick the date, times, and location.',
            ['date', 'start_time', 'end_time', 'location'],
        ),
        (
            'Who can sign up?',
            'Leave the limit blank if there is no maximum number of people.',
            ['max_attendees'],
        ),
        (
            'Contact person',
            'Optional — shown if visitors have questions about this event.',
            ['contact_email', 'contact_phone', 'notes'],
        ),
        (
            'Visibility',
            None,
            ['is_public'],
        ),
    ]

    class Meta:
        model = Event
        fields = [
            'title', 'description', 'category', 'date', 'start_time', 'end_time',
            'location', 'is_public', 'max_attendees', 'contact_email', 'contact_phone', 'notes',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe the event in a few sentences…'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Internal notes for staff (not shown on the website)'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Saturday Community Meal'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. 123 Main St, Jeffersonville'}),
            'max_attendees': forms.NumberInput(attrs={'placeholder': 'Leave blank for no limit', 'min': 1}),
        }
        labels = {
            'title': 'Event name',
            'description': 'Description',
            'category': 'Type of event',
            'date': 'Date',
            'start_time': 'Start time',
            'end_time': 'End time',
            'location': 'Location',
            'is_public': 'Show this event on the public website calendar',
            'max_attendees': 'Maximum number of people',
            'contact_email': 'Contact email',
            'contact_phone': 'Contact phone',
            'notes': 'Staff notes (private)',
        }
        help_texts = {
            'category': 'Optional — helps organize events by type.',
            'is_public': 'Uncheck to hide the event from the website while you are still planning it.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = '— Choose a type (optional) —'


class PostForm(StyledForm):
    field_groups = [
        (
            'Article details',
            'Write your news or update. Choose English or Spanish.',
            ['title', 'language', 'excerpt', 'body'],
        ),
        (
            'Photo',
            'Optional — a picture to show at the top of the article.',
            ['featured_image'],
        ),
        (
            'Related event',
            'Optional — link this article to a specific event.',
            ['related_event'],
        ),
        (
            'Publishing',
            'Check the box below when you are ready for everyone to see this on the website.',
            ['is_published', 'published_at'],
        ),
    ]

    class Meta:
        model = Post
        fields = [
            'title', 'language', 'excerpt', 'body', 'featured_image',
            'related_event', 'is_published', 'published_at',
        ]
        widgets = {
            'body': forms.Textarea(attrs={'rows': 12, 'placeholder': 'Write the full article here…'}),
            'excerpt': forms.Textarea(attrs={'rows': 3, 'placeholder': 'A short summary (optional)'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Thank You to Our Volunteers'}),
            'published_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'title': 'Headline',
            'language': 'Language',
            'excerpt': 'Short summary',
            'body': 'Full article',
            'featured_image': 'Photo',
            'related_event': 'Related event',
            'is_published': 'Publish on the website',
            'published_at': 'Date to show on the article',
        }
        help_texts = {
            'excerpt': 'A brief preview shown in the news list. If left blank, the first part of your article is used.',
            'published_at': 'Usually today\'s date. This is the date visitors see on the article.',
            'is_published': 'Leave unchecked to save as a draft you can finish later.',
            'body': 'Use the formatting buttons to add bold text, lists, and paragraphs.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget = RichTextWidget()
        self.fields['related_event'].empty_label = '— No related event —'
        if not self.instance.pk:
            self.fields['is_published'].initial = False

    def clean_body(self):
        return sanitize_html(self.cleaned_data.get('body', ''))

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.title)[:220]
        if commit:
            instance.save()
        return instance


class SiteContentForm(StyledForm):
    field_groups = [
        (
            'Edit the text',
            'Changes appear on the website after you click Save.',
            ['title', 'body'],
        ),
    ]

    class Meta:
        model = SiteContent
        fields = ['key', 'language', 'title', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 10}),
            'title': forms.TextInput(attrs={'placeholder': 'Optional heading (usually leave blank)'}),
        }
        labels = {
            'key': 'Internal name',
            'language': 'Language',
            'title': 'Heading (optional)',
            'body': 'Text to show on the website',
        }
        help_texts = {
            'title': 'Most sections do not need a heading — only fill this in if you see one on the live page.',
            'body': 'Use the formatting buttons above the text box — you never need to type HTML code.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        key = self.instance.key if self.instance.pk else None
        if self.instance.pk:
            self.fields.pop('key', None)
            self.fields.pop('language', None)
        self._configure_body_field(key)

    def _configure_body_field(self, key):
        body_field = self.fields['body']
        if key in SINGLE_LINE_KEYS:
            body_field.widget = forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. loveunlimitedcommunityoutreach@gmail.com' if key == 'contact-email' else '(502) 509-7563',
            })
            body_field.label = 'Email address' if key == 'contact-email' else 'Phone number'
            body_field.help_text = 'Plain text only — no formatting needed.'
        elif key == 'footer-tagline':
            body_field.widget = forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'rows': 3,
                'placeholder': 'A short sentence for the bottom of every page…',
            })
            body_field.help_text = 'One or two short sentences. No formatting needed.'
        else:
            body_field.widget = RichTextWidget()
            body_field.help_text = (
                'Type normally, like in a word processor. Highlight words and click B to make them bold.'
            )

    def clean_body(self):
        body = self.cleaned_data.get('body', '')
        key = self.instance.key if self.instance.pk else self.cleaned_data.get('key')
        if key in PLAIN_TEXT_KEYS:
            return strip_tags(body).strip()
        if key == 'footer-tagline':
            return strip_tags(body).strip()
        return sanitize_html(body)


class SiteContentCreateForm(SiteContentForm):
    """New blocks are rare — keep key visible for advanced use only."""

    field_groups = [
        (
            'New text section',
            'Only add a new section if your web administrator asked you to.',
            ['key', 'language', 'title', 'body'],
        ),
    ]


class TeamMemberForm(StyledForm):
    field_groups = [
        (
            'Person details',
            None,
            ['name', 'role', 'bio', 'photo'],
        ),
        (
            'Display options',
            None,
            ['ordering', 'is_active'],
        ),
    ]

    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'bio', 'photo', 'ordering', 'is_active']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5}),
            'name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'role': forms.TextInput(attrs={'placeholder': 'e.g. Executive Director'}),
        }
        labels = {
            'name': 'Name',
            'role': 'Job title / role',
            'bio': 'Short biography',
            'photo': 'Photo',
            'ordering': 'Display order',
            'is_active': 'Show on the About Us page',
        }
        help_texts = {
            'ordering': 'Lower numbers appear first. Use 1 for the first person, 2 for the second, and so on.',
            'photo': 'A square photo works best.',
        }


class ResourceForm(StyledForm):
    field_groups = [
        (
            'Organization details',
            None,
            ['category', 'name', 'description'],
        ),
        (
            'How to reach them',
            None,
            ['address', 'phone', 'website', 'hours'],
        ),
        (
            'Listing options',
            None,
            ['tags', 'is_active', 'ordering'],
        ),
    ]

    class Meta:
        model = Resource
        fields = [
            'category', 'name', 'description', 'address', 'phone', 'website',
            'hours', 'tags', 'is_active', 'ordering',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'name': forms.TextInput(attrs={'placeholder': 'Organization or program name'}),
            'tags': forms.TextInput(attrs={'placeholder': 'food, shelter, housing'}),
        }
        labels = {
            'category': 'Category',
            'name': 'Name',
            'description': 'What they offer',
            'address': 'Address',
            'phone': 'Phone number',
            'website': 'Website',
            'hours': 'Hours open',
            'tags': 'Search keywords',
            'is_active': 'Show on the website',
            'ordering': 'Display order',
        }
        help_texts = {
            'tags': 'Separate words with commas — helps people find this when they search.',
            'ordering': 'Lower numbers appear first within the category.',
        }


class ResourceCategoryForm(StyledForm):
    class Meta:
        model = ResourceCategory
        fields = ['name', 'slug', 'icon_class', 'ordering']


class DonationSettingsForm(StyledForm):
    field_groups = [
        (
            'Donation button',
            'This link powers the Donate buttons across your website. Your web administrator can update it if needed.',
            ['zeffy_form_link'],
        ),
        (
            'Tax information',
            None,
            ['tax_id'],
        ),
        (
            'What donations provide',
            'Short sentences shown on the donate page to explain impact.',
            ['impact_25', 'impact_50', 'impact_100'],
        ),
    ]

    class Meta:
        model = DonationSettings
        fields = ['zeffy_form_link', 'tax_id', 'impact_25', 'impact_50', 'impact_100']
        widgets = {
            'zeffy_form_link': forms.URLInput(attrs={'placeholder': 'https://www.zeffy.com/embed/...'}),
            'impact_25': forms.TextInput(attrs={'placeholder': 'e.g. Provides meals for 5 people'}),
            'impact_50': forms.TextInput(attrs={'placeholder': 'e.g. Supplies hygiene kits for 10 families'}),
            'impact_100': forms.TextInput(attrs={'placeholder': 'e.g. Provides emergency shelter for one night'}),
        }
        labels = {
            'zeffy_form_link': 'Zeffy donation link',
            'tax_id': 'Tax ID / EIN number',
            'impact_25': '$25 donation impact',
            'impact_50': '$50 donation impact',
            'impact_100': '$100 donation impact',
        }
        help_texts = {
            'tax_id': 'Shown on the donate page for tax-deductible gifts.',
        }


class EventCategoryForm(StyledForm):
    class Meta:
        model = EventCategory
        fields = ['name', 'color', 'description']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }
