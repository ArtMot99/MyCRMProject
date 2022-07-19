from django.urls import path, include
from crmproject import views


profile_urls = [
    path('', views.MyProfileView.as_view(), name='profile'),
    path('update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('delete/', views.DeleteProfileView.as_view(), name='delete_profile'),
]


company_urls = [
    path('', views.InfoAboutCompany.as_view(), name='info'),
    path('update/', views.UpdateCompany.as_view(), name='update_company'),
    path('delete/', views.DeleteCompanyView.as_view(), name='delete_company'),
]


urlpatterns = [
    path('', views.AllCompanyView.as_view(), name='index'),
    path('info/<int:pk>', include(company_urls)),
    path('profile/<int:pk>', include(profile_urls)),
]
