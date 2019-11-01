from django.urls import path
from .views import LostItemListView, LostItemUpdateView

urlpatterns = [
  path('lost-items', LostItemListView.as_view(), name='lost-items'),
  path('update/<int:pk>', LostItemUpdateView.as_view(), name='update-lost-item'),
  # path('add-found-item', addFoundItemView, name='add-found-item'),
  # path('get-items', getItems, name='get-items'),
]