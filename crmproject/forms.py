from django import forms
from django.core.exceptions import ValidationError

from crmproject.models import Company
from users.models import User


class FormUpdateProfile(forms.ModelForm):
    """
    Form for Update profile settings
    """
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


class FormUpdateCompany(forms.ModelForm):
    """
    Form for Update company settings
    """
    update_at = forms.DateField(required=True)

    class Meta:
        model = Company
        fields = ['name_of_company', 'director_name', 'director_surname',
                  'location', 'about_company', 'photo', 'update_at']
