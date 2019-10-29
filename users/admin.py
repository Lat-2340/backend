from django.contrib import admin

from .models import Organization, Office, CustomUser

admin.site.register([Organization, Office, CustomUser])
