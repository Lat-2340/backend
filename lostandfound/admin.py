from django.contrib import admin

from .models import Item, FoundItem

admin.site.register([Item, FoundItem])