from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from users.forms import UserRegistrationForm


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
