from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

from crmproject.models import Company


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
