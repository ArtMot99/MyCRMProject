from django.urls import path, include
from crmproject import views

urlpatterns = [
    path('', views.AllCompanyView.as_view(), name='index'),
    path('info/<int:pk>', views.InfoAboutCompany.as_view(), name='info'),
    path('profile/<int:pk>', views.MyProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/update', views.UpdateProfileView.as_view(), name='update_profile'),
]
