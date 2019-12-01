import os
import json

from django.core.files import File
import base64

from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from mongoengine import *

from .models import Item

def encode_base64(filepath):
  with open(filepath, 'rb') as f:
    image = File(f)
    data = base64.b64encode(image.read())
    return data

def decode_base64(filename, strData):
  with open(filename, 'wb+') as f:
    data = base64.b64decode(strData)
    f.write(data)

def get_image_filename(itemId):
  return os.getcwd() + "/media/" + str(itemId) + ".jpg"

@api_view(['POST'])
def addItemView(request):
  try:
    data = request.data.dict() # mutable copy of request.data
    img = data['image']
    del data['image']

    item = Item(**data)
    item.user = request.user.username
    item.save()

    decode_base64(get_image_filename(str(item.id)), img)
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
    item = Item.objects(id=request.data['id'], user=request.user.username)
    if len(item) > 1:
      return Response(
        {"error": _("More than one item matched.")},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
    item = item[0]

    data = request.data.dict() # mutable copy of request.data
    if 'image' in data:
      img = data['image']
      del data['image']
      handle_uploaded_file(get_image_filename(str(item.id)), img)

    for k, v in data.items():
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
    item = Item.objects(id=request.data['id'], user=request.user.username)
    if len(item) > 1:
      return Response(
        {"error": _("More than one item matched.")},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
    item = item[0]

    try:
      os.remove(get_image_filename(str(item.id)))
    except FileNotFoundError as e:
      print(e)

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
  items = Item.objects(user=username, is_lost=True)
  objects = [item.to_json() for item in items]
  images = [encode_base64(get_image_filename(str(item.id))) for item in items]
  return Response(
    data={
      'lost_items': objects,
      'lost_images': images,
    },
  )

@api_view(['GET'])
def getFoundItems(request):
  username = request.user.username
  items = Item.objects(user=username, is_lost=False)
  objects = [item.to_json() for item in items]
  images = [encode_base64(get_image_filename(str(item.id))) for item in items]
  return Response(
    data={
      'found_items': objects,
      'found_images': images,
    },
  )