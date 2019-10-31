from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from phonenumber_field.modelfields import PhoneNumberField


# automatically create token for new user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
  if created:
    Token.objects.create(user=instance)

class Organization(models.Model):
  orgname = models.CharField(max_length=30, primary_key=True)

  class Meta:
    db_table = 'Organization'

  def __str__(self):
    return self.orgname

class PickupLocation(models.Model):
  address = models.CharField(max_length=70, primary_key=True)
  org = models.ForeignKey(Organization, on_delete=models.CASCADE)
  office = models.CharField(max_length=30)
  phone_number = PhoneNumberField(blank=True, null=True)
  website = models.URLField(blank=True, null=True)

  class Meta:
    db_table = 'PickupLocation'

  def __str__(self):
    rep = "office: {0}, org: {1}, address: {2}"
    return rep.format(self.office, self.org, self.address)

class CustomUser(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(max_length=20, unique=True)
  email = models.EmailField(null=True, blank=True)
  phone_number = PhoneNumberField(blank=False)
  org = models.ForeignKey(Organization, on_delete=models.CASCADE)

  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  date_joined = models.DateTimeField(default=timezone.now)

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['phone_number', 'org']

  objects = UserManager()

  def __str__(self):
    rep = "username: {0}, org: {1}"
    return rep.format(self.username, self.org)
