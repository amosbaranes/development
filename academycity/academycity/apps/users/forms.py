from django import forms
from django.contrib.auth.forms import (UserCreationForm)
from django.contrib.auth import get_user_model
from .models import (Profile)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


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


