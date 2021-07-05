from django import forms
from django.contrib.auth import get_user_model
from .models import (Profile)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'email'
        )


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', 'date_of_birth', 'short_bio', 'bio',
                  'address', 'zip', 'city', 'country',
                  'phone', 'website', 'institution')


