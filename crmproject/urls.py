from django.conf import settings
from django.urls import path, include
from crmproject import views


interaction_urls = [
    path('', views.AboutInteractionView.as_view(), name='about_interaction'),
    path('update/', views.UpdateInteractionView.as_view(), name='update_interaction'),
    path('delete/', views.DeleteInteractionView.as_view(), name='delete_interaction'),
]


profile_urls = [
    path('', views.MyProfileView.as_view(), name='profile'),
    path('update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('delete/', views.DeleteProfileView.as_view(), name='delete_profile'),
    path('my_interaction/', views.InfoAboutMyInteractionView.as_view(), name='my_interaction'),
    path('create_company/', views.CreateCompanyView.as_view(), name='create_company'),
]


projects_urls = [
    path('', views.ProjectInfoView.as_view(), name='about_project'),
    path('create_interaction/', views.CreateInteractionView.as_view(), name='create_interaction'),
    path('update/', views.UpdateProjectView.as_view(), name='update_project'),
    path('delete/', views.DeleteProjectView.as_view(), name='delete_project'),
    path('interaction/<int:interaction_pk>/', include(interaction_urls)),
]


company_urls = [
    path('', views.InfoAboutCompanyView.as_view(), name='info'),
    path('update/', views.UpdateCompanyView.as_view(), name='update_company'),
    path('delete/', views.DeleteCompanyView.as_view(), name='delete_company'),
    path('create_project/', views.CreateProjectView.as_view(), name='create_project'),
    path('project/<int:project_pk>/', include(projects_urls)),
]


urlpatterns = [
    path('', views.AllCompanyView.as_view(), name='index'),
    path('info/<int:pk>/', include(company_urls)),
    path('profile/', include(profile_urls)),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
