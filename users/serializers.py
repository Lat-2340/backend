from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserModel
    fields = ['username', 'password', 'email', 'phone_number', 'org']
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    user = UserModel(**validated_data)
    user.set_password(validated_data['password'])
    user.save()
    return user