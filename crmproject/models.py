from django.contrib.auth import get_user_model
from django.db import models
from users.models import User


class Company(models.Model):
    name_of_company = models.CharField(max_length=50)
    director_name = models.CharField(max_length=20)
    director_surname = models.CharField(max_length=20)
    director_patronymic = models.CharField(max_length=20)
    about_company = models.TextField(max_length=500)
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
    phone_number = models.CharField(max_length=12, verbose_name='Номер телефона')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f'Phone: {self.phone_number} | Name: {self.company}'


class Email(models.Model):
    email_address = models.EmailField(max_length=100, verbose_name='Email адрес')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f'Email: {self.email_address} | Name: {self.company}'
