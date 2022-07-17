from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView, TemplateView, ListView
from django.views.generic.detail import SingleObjectMixin
from users.forms import UserRegistrationForm
from users.models import User


class HomeView(TemplateView):
    template_name = 'home.html'


class RegistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            return self.form_invalid(form)
