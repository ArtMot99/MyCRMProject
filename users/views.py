from django.shortcuts import render
from django.views.generic import FormView, TemplateView, ListView
from django.views.generic.detail import SingleObjectMixin
from users.forms import UserRegistrationForm
from users.models import User


class HomeView(TemplateView):
    template_name = 'home.html'


class RegistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = '../'


class ProfileView(SingleObjectMixin, ListView):
    model = User
    template_name = 'registration/profile.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=User.objects.all())
        return super().get(request, *args, **kwargs)
