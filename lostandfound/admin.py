from django.contrib import admin
from .models import PickupLocation, LostItem, FoundItem

admin.site.register(PickupLocation)
admin.site.register(LostItem)
admin.site.register(FoundItem)