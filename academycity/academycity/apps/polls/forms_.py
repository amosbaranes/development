from django import forms

from .models import Poll


class PollWizardForm(forms.ModelForm):
    class Meta:
        model = Poll
        exclude = []