from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from crmproject.models import Company, Phone, Email, Project
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


class CreateCompanyForm(forms.ModelForm):
    """
    Form for Create company info
    """
    class Meta:
        model = Company
        fields = ['name_of_company', 'director_name', 'director_surname', 'director_patronymic',
                  'about_company', 'location', 'photo']


class PhoneForm(forms.ModelForm):
    """
    Form for Create phone number
    """
    class Meta:
        model = Phone
        fields = ['phone_number']

    def clean_phone_number(self):
        phone_num = self.cleaned_data['phone_number']
        if not phone_num.isdigit() or len(phone_num) != 12:
            raise ValidationError('Phone number must have only digits and must have 12 symbols')
        return phone_num


class EmailForm(forms.ModelForm):
    """
    Form for Create email address
    """
    class Meta:
        model = Email
        fields = ['email_address']


CompanyPhoneFormSet = inlineformset_factory(Company, Phone,
                                            form=PhoneForm,
                                            can_delete=False,
                                            extra=2)
CompanyEmailFormSet = inlineformset_factory(Company, Email,
                                            form=EmailForm,
                                            can_delete=False,
                                            extra=2,)

CompanyPhoneForUpdate = inlineformset_factory(Company, Phone,
                                              form=PhoneForm,
                                              can_delete=True,
                                              extra=2)
CompanyEmailForUpdate = inlineformset_factory(Company, Email,
                                              form=EmailForm,
                                              can_delete=True,
                                              extra=2)


class UpdateCompanyForm(forms.ModelForm):
    """
    Form for Update company info
    """
    update_at = forms.DateField(required=True)

    class Meta:
        model = Company
        fields = ['name_of_company', 'director_name', 'director_surname',
                  'location', 'about_company', 'photo', 'update_at']


class CreateProjectForm(forms.ModelForm):
    """
    Form for Create project info
    """

    class Meta:
        model = Project
        fields = ['name', 'date_start', 'date_end', 'price', 'description']
