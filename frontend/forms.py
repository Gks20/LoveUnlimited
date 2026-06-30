from django import forms

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True, label="First Name")
    last_name = forms.CharField(max_length=50, required=True, label="Last Name")
    email = forms.EmailField(max_length=120, required=True, label="Email Address")
    phone = forms.CharField(max_length=25, required=False, label="Phone Number")
    subject = forms.ChoiceField(
        choices=[
            ("volunteer", "Volunteer Opportunities"),
            ("donate", "Donation Questions"),
            ("services", "Services Information"),
            ("partnership", "Partnership Inquiry"),
            ("media", "Media Inquiry"),
            ("other", "Other"),
        ],
        required=True,
        label="Subject"
    )
    message = forms.CharField(widget=forms.Textarea(attrs={"rows":5}), required=True, label="Message")

    def clean_message(self):
        msg = self.cleaned_data['message']
        if len(msg.strip()) < 10:
            raise forms.ValidationError("Message must be at least 10 characters for sufficient detail.")
        return msg
