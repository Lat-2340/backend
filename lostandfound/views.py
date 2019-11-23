from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from mongoengine import *

from .models import Item

@api_view(['POST'])
def addItemView(request):
  try:
    item = Item(**request.data)
    item.user = request.user.username
    item.save()
    print(item.id, item)
  except (ValidationError, FieldDoesNotExist) as e:
    return Response(
      {"error": _(str(e))},
      status=status.HTTP_400_BAD_REQUEST
    )
  return Response(
    {"detail": _("Added item %s." % item.id)},
    status=status.HTTP_201_CREATED
  )

# TODO: CRUD APIs

@api_view(['GET'])
def getItems(request):
  # TODO: separate getter for lost and found items
  username = request.user.username
  items = [item.to_json() for item in Item.objects(user=username)]
  print(items)
  return Response(
    data={
      'items': items,
    },
  )