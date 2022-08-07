from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views.generic.detail import SingleObjectMixin, DetailView
from crmproject.forms import FormUpdateProfile, CreateCompanyForm, CompanyPhoneFormSet, \
    CompanyEmailFormSet, CompanyPhoneForUpdate, CompanyEmailForUpdate, UpdateCompanyForm, CreateProjectForm, \
    UpdateProjectForm, CreateInteractionForm
from crmproject.models import Company, Project, Interaction
from users.models import User


class MyProfileView(LoginRequiredMixin, DetailView):
    """
    View for view the user's personal settings
    """
    model = User
    template_name = 'crmproject/profile.html'

    def get_object(self, queryset=None):
        """
        Redefinition method

        :param queryset: None
        :return: self.request.user
        """
        return self.request.user


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
    View for update user information
    """
    template_name = 'crmproject/update_profile.html'
    model = User
    form_class = FormUpdateProfile

    def get_object(self, queryset=None):
        """
        Redefinition method

        :param queryset: None
        :return: self.request.user
        """
        return self.request.user

    def get_success_url(self):
        """
        Redefinition method

        After updating information about yourself, the user will be redirected to profile
        :return: reverse_lazy('profile')
        """
        return reverse_lazy('profile')


class DeleteProfileView(DeleteView):
    """
    View for delete user
    """
    model = User
    success_url = reverse_lazy('home')
    template_name = 'crmproject/profile_delete.html'

    def get_object(self, queryset=None):
        """
        Redefinition method

        :param queryset: None
        :return: self.request.user
        """
        return self.request.user


class InfoAboutMyInteractionView(LoginRequiredMixin, SingleObjectMixin, ListView):
    """
    View for show my interactions
    """
    model = Interaction
    template_name = 'crmproject/my_interaction.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        """
        Redefinition method

        Get a queryset of all interactions into a variable 'self.object'
        :param request: request
        :param args: *
        :param kwargs: **
        :return: super().get(request, *args, **kwargs)
        """
        self.object = Interaction.objects.all()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Redefinition method

        Filtering and showing the user a list of his interactions
        :return: Interaction.objects.filter(manager=self.request.user)
        """
        return Interaction.objects.filter(manager=self.request.user)


class AllCompanyView(LoginRequiredMixin, ListView):
    """
    View for list all available companies with pagination
    """
    model = Company
    template_name = 'crmproject/index.html'
    context_object_name = 'companys'
    paginate_by = 6

    # def get_ordering(self):
    #     ordering = self.request.GET.get('sort', 'a')
    #     if ordering == 'a':
    #         return 'name_of_company'
    #     else:
    #         return '-name_of_company'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(cnt=Count('project'))
        return qs


class InfoAboutCompanyView(LoginRequiredMixin, SingleObjectMixin, ListView):
    """
    View for view detailed information about the company
    """
    model = Project
    template_name = 'crmproject/info_about_company.html'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        """
        Redefinition method

        In a variable self.object we get queryset
        :param request: request
        :param args: *
        :param kwargs: **
        :return: super().get(request, *args, **kwargs)
        """
        self.object = Company.objects.get(pk=self.kwargs['pk'])
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = Project.objects.all()
        qs = qs.annotate(cnt=Count('interaction'))
        return qs


class CreateCompanyView(LoginRequiredMixin, CreateView):
    """
    View for create company information
    """
    model = Company
    form_class = CreateCompanyForm
    template_name = 'crmproject/create_company.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        """
        Redefinition method

        The method displays 2 additional forms for adding phone numbers and email addresses
        :param kwargs: **
        :return: context
        """
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
        """
        Redefinition method

        Checking forms for validity
        :param form: form
        :return: super().form_valid(form)
        """
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
        """
        Redefinition method

        After updating the company information, the user will be redirected to the company information page
        :return: reverse_lazy('info', kwargs={'pk': self.kwargs['pk']})
        """
        return reverse_lazy('info', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        """
        Redefinition method

        Only the user who created the company can update information about it
        :return: True or False
        """
        if self.request.user != self.get_object(queryset=Company.objects.all()).user:
            return False
        return True

    def get_context_data(self, **kwargs):
        """
        Redefinition method

        Shows the user data from the database in forms to update information about companies
        :param kwargs: **
        :return: context
        """
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
        """
        Redefinition method

        Checking forms for validity
        :param form: form
        :return: super().form_valid(form)
        """
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
    model = Interaction
    template_name = 'crmproject/info_about_project.html'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        """
        Redefinition method

        In a variable self.object we get queryset
        :param request: request
        :param args: *
        :param kwargs: **
        :return: super().get(request, *args, **kwargs)
        """
        self.object = Project.objects.get(pk=self.kwargs['project_pk'])
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Redefinition method

        We get a queryset with filtered interactions for each project
        :return: Project.objects.filter(company=self.kwargs['project_pk'])
        """
        return Interaction.objects.filter(project=self.kwargs['project_pk'])


class CreateProjectView(LoginRequiredMixin, CreateView):
    """
    View for Create info about project
    """
    model = Project
    form_class = CreateProjectForm
    template_name = 'crmproject/create_project.html'

    def get_success_url(self):
        """
        Redefinition method

        After creating the project, the user will be redirected to the page for viewing information about the company
        :return: reverse_lazy('info', kwargs={'pk': self.kwargs['pk']})
        """
        return reverse_lazy('info', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        """
        Redefinition method

        Checking forms for validity
        :param form: form
        :return: super().form_valid(form)
        """
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
    pk_url_kwarg = 'project_pk'

    def get_success_url(self):
        """
        Redefinition method

        After updating the information about the project,
        the user will be redirected to the page for viewing information about the project
        :return: self.object.get_absolute_url()
        """
        return self.object.get_absolute_url()


class DeleteProjectView(LoginRequiredMixin, DeleteView):
    """
    View for delete project information
    """
    model = Project
    template_name = 'crmproject/project_delete.html'
    pk_url_kwarg = 'project_pk'

    def get_success_url(self):
        """
        Redefinition method

        After deleted project, the user will be redirected to the page for viewing information about the company
        :return: reverse_lazy('info', kwargs={'pk': self.object.company_id})
        """
        return reverse_lazy('info', kwargs={'pk': self.object.company.pk})


class AboutInteractionView(LoginRequiredMixin, DetailView):
    """
    View for view detailed information about interaction
    """
    model = Interaction
    template_name = 'crmproject/info_about_interaction.html'
    pk_url_kwarg = 'interaction_pk'


class CreateInteractionView(LoginRequiredMixin, CreateView):
    """
    View for Create interaction on project
    """
    model = Interaction
    form_class = CreateInteractionForm
    template_name = 'crmproject/create_interaction.html'

    def get_success_url(self):
        """
        Redefinition method

        After adding the interaction, the user will be redirected to the page for viewing information about the project
        :return: self.object.project.get_absolute_url()
        """
        return self.object.project.get_absolute_url()

    def form_valid(self, form):
        """
        Redefinition method

        Checking forms for validity
        :param form: form
        :return: super().form_valid(form)
        """
        f = form.save(commit=False)
        f.manager = self.request.user
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        f.project = project
        f.save()
        return super().form_valid(form)


class UpdateInteractionView(LoginRequiredMixin, UpdateView):
    """
    View for Update interaction on project
    """
    model = Interaction
    form_class = CreateInteractionForm
    template_name = 'crmproject/create_interaction.html'
    pk_url_kwarg = 'interaction_pk'

    def get_success_url(self):
        """
        Redefinition method

        After updated the interaction, the user will be redirected to the page for viewing information about the project
        :return: self.object.project.get_absolute_url()
        """
        return self.object.project.get_absolute_url()

    def form_valid(self, form):
        """
        Redefinition method

        Checking forms for validity
        :param form: form
        :return: super().form_valid(form)
        """
        f = form.save(commit=False)
        f.manager = self.request.user
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        f.project = project
        f.save()
        return super().form_valid(form)


class DeleteInteractionView(LoginRequiredMixin, DeleteView):
    model = Interaction
    template_name = 'crmproject/interaction_delete.html'
    pk_url_kwarg = 'interaction_pk'

    def get_success_url(self):
        """
        Redefinition method

        After deleted the interaction, the user will be redirected to the page for viewing information about the project
        :return: self.object.project.get_absolute_url()
        """
        return reverse_lazy('about_project', kwargs={'pk': self.object.project.company.pk,
                                                     'project_pk': self.object.project.pk})
