from django.urls import path
from . import views

urlpatterns = [
  path('add-item', views.addItemView, name='add-item'),
  path('update-item', views.updateItemView, name='update-item'),
  path('delete-item', views.deleteItemView, name='delete-item'),
  path('get-lost-items', views.getUserLostItems, name='get-lost-items'),
  path('get-found-items', views.getUserFoundItems, name='get-found-items'),
  path('get-matched-items', views.getMatchedFoundItems, name='get-matched-items'),
]