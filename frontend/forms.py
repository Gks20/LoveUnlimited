from django import forms

from frontend.localized import localized_text


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=120, required=True)
    phone = forms.CharField(max_length=25, required=False)
    subject = forms.ChoiceField(choices=[], required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = localized_text('ui-form-first-name', 'First Name')
        self.fields['last_name'].label = localized_text('ui-form-last-name', 'Last Name')
        self.fields['email'].label = localized_text('ui-form-email', 'Email Address')
        self.fields['phone'].label = localized_text('ui-form-phone', 'Phone Number')
        self.fields['subject'].label = localized_text('ui-form-subject', 'Subject')
        self.fields['message'].label = localized_text('ui-form-message', 'Message')
        self.fields['subject'].choices = [
            ('volunteer', localized_text('ui-form-subject-volunteer', 'Volunteer Opportunities')),
            ('donate', localized_text('ui-form-subject-donate', 'Donation Questions')),
            ('services', localized_text('ui-form-subject-services', 'Services Information')),
            ('partnership', localized_text('ui-form-subject-partnership', 'Partnership Inquiry')),
            ('media', localized_text('ui-form-subject-media', 'Media Inquiry')),
            ('other', localized_text('ui-form-subject-other', 'Other')),
        ]

    def clean_message(self):
        msg = self.cleaned_data['message']
        if len(msg.strip()) < 10:
            raise forms.ValidationError(
                localized_text(
                    'ui-form-message-min',
                    'Message must be at least 10 characters for sufficient detail.',
                )
            )
        return msg
