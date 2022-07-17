from django.urls import path, include
from crmproject import views

urlpatterns = [
    path('', views.AllCompanyView.as_view(), name='index'),
    path('info/<int:pk>', views.InfoAboutCompany.as_view(), name='info'),
]
