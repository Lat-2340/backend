from django.utils.translation import ugettext_lazy as _

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Item, FoundItem
from .serializers import ItemSerializer, FoundItemSerializer

class LostItemListView(generics.ListCreateAPIView):
  serializer_class = ItemSerializer

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  def get_queryset(self):
    return Item.objects.filter(user=self.request.user)

class LostItemUpdateView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = ItemSerializer

  def get_queryset(self):
    return Item.objects.filter(user=self.request.user)

class FoundItemListView(generics.ListCreateAPIView):
  serializer_class = FoundItemSerializer

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  def get_queryset(self):
    return FoundItem.objects.filter(user=self.request.user)

class FoundItemUpdateView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = FoundItemSerializer

  def get_queryset(self):
    return FoundItem.objects.filter(user=self.request.user)