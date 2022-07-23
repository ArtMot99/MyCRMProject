from django.contrib import admin
from crmproject.models import Company, Phone, Email, Project, Interaction

admin.site.register(Company)
admin.site.register(Phone)
admin.site.register(Email)
admin.site.register(Project)
admin.site.register(Interaction)