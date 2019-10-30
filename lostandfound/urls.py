from django.urls import path
from .views import indexView, addLostItemView, addFoundItemView

urlpatterns = [
  path('', indexView, name='index'),
  path('lost-item/', addLostItemView, name='add-lost-item'),
  path('found-item/', addFoundItemView, name='add-found-item'),
]