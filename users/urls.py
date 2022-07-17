from django.urls import path, include
from django.views.generic import TemplateView

from users import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.RegistrationView.as_view(), name='registration'),
]
