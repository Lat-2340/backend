from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Organization
from lostandfound.models import Item

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = UserModel
    fields = ['username', 'password', 'email', 'phone_number', 'org']
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    o = validated_data.pop('org')
    org_instance = Organization.objects.get(orgname=o)
    user = UserModel(org=org_instance, **validated_data)
    user.set_password(validated_data['password'])
    user.save()
    return user