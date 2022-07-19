from django.contrib.auth import get_user_model
from django.db import models
from users.models import User
from ckeditor.fields import RichTextField


class Company(models.Model):
    """
    Model for Company in crmproject app.
    """
    name_of_company = models.CharField(max_length=50)
    director_name = models.CharField(max_length=20)
    director_surname = models.CharField(max_length=20)
    director_patronymic = models.CharField(max_length=20)
    about_company = RichTextField(blank=True, null=True)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=30)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/photos', default='', blank=True)

    class Meta:
        ordering = ('name_of_company',)

    def __str__(self):
        return self.name_of_company


class Phone(models.Model):
    """
    Model for Phone for inlineformset
    """
    phone_number = models.CharField(max_length=12, verbose_name='Номер телефона')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f'Phone: {self.phone_number} | Company: {self.company}'


class Email(models.Model):
    """
    Model for Email for inlineformset
    """
    email_address = models.EmailField(max_length=100, verbose_name='Email адрес')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f'Email: {self.email_address} | Company: {self.company}'
