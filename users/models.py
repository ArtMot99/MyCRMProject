from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=120, unique=True)
    birthday = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=30, null=True, blank=True)
    photo = models.ImageField(upload_to='users/photos', default='', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('first_name',)

    def __str__(self):
        return self.username

