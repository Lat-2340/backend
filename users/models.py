from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

class Organization(models.Model):
  orgname = models.CharField(max_length=30, primary_key=True)

  def __str__(self):
    return self.orgname

class CustomUser(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(max_length=20, unique=True)
  email = models.EmailField(blank=False)
  phone_number = PhoneNumberField(null=True, blank=True)
  org_userid = models.CharField(max_length=10, help_text="id number at your organization") # QUESTION remove this field?
  org = models.ForeignKey(Organization, on_delete=models.CASCADE)

  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  date_joined = models.DateTimeField(default=timezone.now)

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email', 'org']

  objects = UserManager()

  def __str__(self):
    rep = "username: {0}, org: {1}"
    return rep.format(self.username, self.org)
