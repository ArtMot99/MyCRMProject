from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views.generic.detail import SingleObjectMixin

from crmproject.forms import FormUpdateProfile, FormUpdateCompany, CreateCompanyForm, CompanyPhoneFormSet, \
    CompanyEmailFormSet, CompanyPhoneForUpdate, CompanyEmailForUpdate
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


class InfoAboutCompanyView(LoginRequiredMixin, SingleObjectMixin, ListView):
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


class CreateCompanyView(LoginRequiredMixin, CreateView):
    """
    View for create company information
    """
    model = Company
    form_class = CreateCompanyForm
    template_name = 'crmproject/create_company.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            contact_phone = CompanyPhoneFormSet(self.request.POST)
            contact_email = CompanyEmailFormSet(self.request.POST)
        else:
            contact_phone = CompanyPhoneFormSet()
            contact_email = CompanyEmailFormSet()
        context.update(
            {
                'phone_form': contact_phone,
                'email_form': contact_email
            }
        )
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        contact_phone = CompanyPhoneFormSet(self.request.POST)
        contact_email = CompanyEmailFormSet(self.request.POST)
        if contact_email.is_valid() and contact_phone.is_valid():
            self.obj = form.save()
            contact_email.instance = self.obj
            contact_phone.instance = self.obj
            contact_email.save()
            contact_phone.save()
        else:
            return self.form_invalid(form)

        return super().form_valid(form)


class UpdateCompanyView(UserPassesTestMixin, UpdateView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            contact_phone = CompanyPhoneForUpdate(self.request.POST, instance=self.object)
            contact_email = CompanyEmailForUpdate(self.request.POST, instance=self.object)
        else:
            contact_phone = CompanyPhoneForUpdate(instance=self.object)
            contact_email = CompanyEmailForUpdate(instance=self.object)
        context.update(
            {
                'phone_form': contact_phone,
                'email_form': contact_email
            }
        )
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        contact_phone = CompanyPhoneForUpdate(self.request.POST, instance=self.object)
        contact_email = CompanyEmailForUpdate(self.request.POST, instance=self.object)
        if contact_email.is_valid() and contact_phone.is_valid():
            form.save()
            contact_email.save()
            contact_phone.save()
        else:
            return self.form_invalid(form)

        return super().form_valid(form)


class DeleteCompanyView(DeleteView):
    """
    View for delete company
    """
    model = Company
    success_url = reverse_lazy('index')
    template_name = 'crmproject/company_delete.html'

