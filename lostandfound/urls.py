from django.urls import path
from .views import *

urlpatterns = [
  path('lost-items', LostItemListView.as_view(), name='lost-items'),
  path('update-lost-item/<int:pk>', LostItemUpdateView.as_view(), name='update-lost-item'),
  path('found-items', FoundItemListView.as_view(), name='found-items'),
  path('update-found-item/<int:pk>', FoundItemUpdateView.as_view(), name='update-found-item'),
]