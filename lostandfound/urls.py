from django.urls import path
from .views import indexView, addLostItemView

urlpatterns = [
  path('', indexView, name='index'),
  path('lost-item/', addLostItemView, name='add-lost-item'),
]