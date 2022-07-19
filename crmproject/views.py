from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from crmproject.forms import FormUpdateProfile
from crmproject.models import Company
from users.models import User


class AllCompanyView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'crmproject/index.html'
    context_object_name = 'companys'
    paginate_by = 5


class InfoAboutCompany(LoginRequiredMixin, SingleObjectMixin, ListView):
    model = Company
    template_name = 'crmproject/info_about_company.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Company.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.object
        return context


class MyProfileView(LoginRequiredMixin, SingleObjectMixin, ListView):
    model = User
    template_name = 'crmproject/profile.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=User.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = self.object
        return context


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'crmproject/update_profile.html'
    model = User
    form_class = FormUpdateProfile
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
