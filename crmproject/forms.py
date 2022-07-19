from django import forms
from django.core.exceptions import ValidationError
from users.models import User


class FormUpdateProfile(forms.ModelForm):
    username = forms.CharField(error_messages={'required': ''})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'birthday', 'location', 'photo', 'email']

    def clean_first_name(self):
        new_first_name = self.cleaned_data['first_name']
        if not new_first_name[0].isupper():
            raise ValidationError('First letter in name must be upper and name must be string!')
        return new_first_name

    def clean_last_name(self):
        new_last_name = self.cleaned_data['last_name']
        if not new_last_name[0].isupper():
            raise ValidationError('First letter in surname must be upper and surname must be string!')
        return new_last_name


