from django.urls import path
from . import views

urlpatterns = [
  path('add-item', views.addItemView, name='add-item'),
  path('update-item', views.updateItemView, name='update-item'),
  path('delete-item', views.deleteItemView, name='delete-item'),
  path('get-user-lost-items', views.getUserLostItems, name='get-user-lost-items'),
  path('get-user-found-items', views.getUserFoundItems, name='get-user-found-items'),
  path('get-matched-found-items', views.getMatchedFoundItems, name='get-matched-found-items'),
]