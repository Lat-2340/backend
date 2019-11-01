from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Item, FoundItem

UserModel = get_user_model()

class ItemSerializer(serializers.ModelSerializer):
  user = serializers.ReadOnlyField(source='user.username')

  class Meta:
    model = Item
    fields = '__all__'

