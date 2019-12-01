import os

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from mongoengine import *

from .models import Item

def get_image_filename(itemId):
  return os.getcwd() + "/media/" + str(itemId) + ".jpg"

def handle_uploaded_file(filename, f):
  with open(filename, 'wb+') as destination:
    for chunk in f.chunks():
      destination.write(chunk)

@api_view(['POST'])
def addItemView(request):
  try:
    item = Item(**request.POST)
    item.user = request.user.username
    item.save()

    handle_uploaded_file(get_image_filename(str(item.id)), request.FILES['image'])

    item.save()
    print("Added item: ", item.id, item)
  except (ValidationError, FieldDoesNotExist) as e:
    return Response(
      {"error": _(str(e))},
      status=status.HTTP_400_BAD_REQUEST
    )
  return Response(
    {"detail": _("Added item %s." % item.id)},
    status=status.HTTP_201_CREATED
  )

@api_view(['POST'])
def updateItemView(request):
  try:
    item = Item.objects(id=request.POST["id"], user=request.user.username)
    if len(item) > 1:
      return Response(
        {"error": _("More than one item matched.")},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
    item = item[0]

    for k, v in request.POST.items():
      item[k] = v
    print("Updated item: ", item.id, item)
    item.save()
  except (KeyError, IndexError, ValidationError, FieldDoesNotExist) as e:
    return Response(
      {"error": _(str(e))},
      status=status.HTTP_400_BAD_REQUEST
    )
  return Response(
    {"detail": _("Updated item %s." % item.id)},
    status=status.HTTP_200_OK
  )

@api_view(['DELETE'])
def deleteItemView(request):
  try:
    item = Item.objects(id=request.POST["id"], user=request.user.username)
    if len(item) > 1:
      return Response(
        {"error": _("More than one item matched.")},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
    item = item[0]

    os.remove(get_image_filename(str(item.id)))
    item.delete()
  except (KeyError, IndexError, ValidationError, FieldDoesNotExist) as e:
    return Response(
      {"error": _(str(e))},
      status=status.HTTP_400_BAD_REQUEST
    )
  return Response(
    {"detail": _("Deleted item %s." % item.id)},
    status=status.HTTP_204_NO_CONTENT
  )

@api_view(['GET'])
def getLostItems(request):
  username = request.user.username
  items = [item.to_json() for item in Item.objects(user=username, is_lost=True)]
  return Response(
    data={
      'lost_items': items,
    },
  )

@api_view(['GET'])
def getFoundItems(request):
  username = request.user.username
  items = [item.to_json() for item in Item.objects(user=username, is_lost=False)]
  return Response(
    data={
      'found_items': items,
    },
  )