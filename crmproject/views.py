from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views.generic.detail import SingleObjectMixin

from crmproject.forms import FormUpdateProfile, CreateCompanyForm, CompanyPhoneFormSet, \
    CompanyEmailFormSet, CompanyPhoneForUpdate, CompanyEmailForUpdate, UpdateCompanyForm, CreateProjectForm, \
    UpdateProjectForm
from crmproject.models import Company, Project
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


# TODO Don't work pagination(show all queryset objects)
class InfoAboutCompanyView(LoginRequiredMixin, SingleObjectMixin, ListView):
    """
    View for view detailed information about the company
    """
    model = Company
    template_name = 'crmproject/info_about_company.html'
    # paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Company.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.object
        return context

    # def get_queryset(self):
    #     return self.object.project_set.all()


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
    form_class = UpdateCompanyForm

    def get_success_url(self):
        return reverse_lazy('info', kwargs={'pk': self.kwargs['pk']})

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


class DeleteCompanyView(LoginRequiredMixin, DeleteView):
    """
    View for delete company
    """
    model = Company
    success_url = reverse_lazy('index')
    template_name = 'crmproject/company_delete.html'


class ProjectInfoView(LoginRequiredMixin, SingleObjectMixin, ListView):
    """
    View for view detailed information about the projects
    """
    model = Project
    template_name = 'crmproject/info_about_project.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Project.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object
        return context


class CreateProjectView(LoginRequiredMixin, CreateView):
    """
    View for Create info about project
    """
    model = Project
    form_class = CreateProjectForm
    template_name = 'crmproject/create_project.html'

    def get_success_url(self):
        return reverse_lazy('info', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        f = form.save(commit=False)
        f.user = self.request.user
        company = get_object_or_404(Company, pk=self.kwargs['pk'])
        f.company = company
        f.save()
        return super().form_valid(form)


class UpdateProjectView(LoginRequiredMixin, UpdateView):
    """
    View for Update info about project
    """
    model = Project
    form_class = UpdateProjectForm
    template_name = 'crmproject/update_project.html'

    def get_success_url(self):
        return reverse_lazy('about_project', kwargs={'pk': self.kwargs['pk']})


# TODO problem with success_url method(need redirect to info:pk)
class DeleteProjectView(LoginRequiredMixin, DeleteView):
    """
    View for delete project information
    """
    model = Project
    template_name = 'crmproject/project_delete.html'

    def get_success_url(self):
        return reverse_lazy('index')
