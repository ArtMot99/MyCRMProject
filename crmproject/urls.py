from django.urls import path, include
from crmproject import views


profile_urls = [
    path('', views.MyProfileView.as_view(), name='profile'),
    path('update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('delete/', views.DeleteProfileView.as_view(), name='delete_profile'),
]


company_urls = [
    path('', views.InfoAboutCompanyView.as_view(), name='info'),
    path('update/', views.UpdateCompanyView.as_view(), name='update_company'),
    path('delete/', views.DeleteCompanyView.as_view(), name='delete_company'),
]


projects_urls = [
    path('', views.ProjectInfoView.as_view(), name='about_project'),
]


urlpatterns = [
    path('', views.AllCompanyView.as_view(), name='index'),
    path('info/<int:pk>/', include(company_urls)),
    path('profile/<int:pk>/', include(profile_urls)),
    path('project/<int:pk>/', include(projects_urls)),
    path('create_company/', views.CreateCompanyView.as_view(), name='create_company'),
]
