from django.urls import path
from .views import addItemView, getItems

urlpatterns = [
  path('add-item', addItemView, name='add-item'),
  path('get-items', getItems, name='get-items'),
]