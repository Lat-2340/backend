from django.contrib import admin

from .models import Organization, PickupLocation, CustomUser

admin.site.register([Organization, PickupLocation, CustomUser])
