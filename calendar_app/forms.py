from django import forms
from .models import EventRegistration


class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['first_name', 'last_name', 'email', 'phone', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
