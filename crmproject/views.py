from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin

from crmproject.forms import FormUpdateProfile, FormUpdateCompany
from crmproject.models import Company
from users.models import User


class MyProfileView(LoginRequiredMixin, SingleObjectMixin, ListView):
    """
    View for view the user's personal settings
    """
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
    """
    View for update user information
    """
    template_name = 'crmproject/update_profile.html'
    model = User
    form_class = FormUpdateProfile
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class DeleteProfileView(DeleteView):
    """
    View for delete user
    """
    model = User
    success_url = reverse_lazy('index')
    template_name = 'crmproject/profile_delete.html'


class AllCompanyView(LoginRequiredMixin, ListView):
    """
    View for list all available companies with pagination
    """
    model = Company
    template_name = 'crmproject/index.html'
    context_object_name = 'companys'
    paginate_by = 6


class InfoAboutCompany(LoginRequiredMixin, SingleObjectMixin, ListView):
    """
    View for view detailed information about the company
    """
    model = Company
    template_name = 'crmproject/info_about_company.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Company.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.object
        return context


class UpdateCompany(UserPassesTestMixin, UpdateView):
    """
    View for update company information
    """
    template_name = 'crmproject/update_company.html'
    model = Company
    form_class = FormUpdateCompany
    success_url = reverse_lazy('index')

    def test_func(self):
        if self.request.user != self.get_object(queryset=Company.objects.all()).user:
            return False
        return True

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class DeleteCompanyView(DeleteView):
    """
    View for delete company
    """
    model = Company
    success_url = reverse_lazy('index')
    template_name = 'crmproject/company_delete.html'

