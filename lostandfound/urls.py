from django.urls import path
from .views import addItemView, updateItemView, deleteItemView, getLostItems, getFoundItems

urlpatterns = [
  path('add-item', addItemView, name='add-item'),
  path('update-item', updateItemView, name='update-item'),
  path('delete-item', deleteItemView, name='delete-item'),
  path('get-lost-items', getLostItems, name='get-lost-items'),
  path('get-found-items', getFoundItems, name='get-found-items'),
]