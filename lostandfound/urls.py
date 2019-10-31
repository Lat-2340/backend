from django.urls import path
from .views import indexView, addLostItemView, addFoundItemView, getItems

urlpatterns = [
  path('', indexView, name='index'),
  path('add-lost-item', addLostItemView, name='add-lost-item'),
  path('add-found-item', addFoundItemView, name='add-found-item'),
  path('get-items', getItems, name='get-items'),
]