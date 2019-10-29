from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserModel
    fields = ['username', 'password', 'email', 'phone_number', 'org_userid', 'org']
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    user = UserModel.objects.create(
      username = validated_data['username'],
      email = validated_data['email'],
      phone_number = validated_data['phone_number'],
      org_userid = validated_data['org_userid'],
      org = validated_data['org']
    )
    user.set_password(validated_data['password'])
    user.save()
    return user