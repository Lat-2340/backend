from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from mongoengine import *

from .models import Item
from .utils import encode_base64, decode_base64, get_image_filename

@api_view(['POST'])
def addItemView(request):
  try:
    data = request.data.dict() # mutable copy of request.data

    if 'image' not in data:
      return Response(
        {"error": _("An image of the item is required")},
        status=status.HTTP_400_BAD_REQUEST
      )

    img = data['image']
    del data['image']

    item = Item(**data)
    item.user = request.user.username
    item.save()

    decode_base64(get_image_filename(str(item.id), item.is_lost), img)
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
      handle_uploaded_file(get_image_filename(str(item.id), item.is_lost), img)

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
      os.remove(get_image_filename(str(item.id), item.is_lost))
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
  images = [encode_base64(get_image_filename(str(item.id)), item.is_lost) for item in items]
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
  images = [encode_base64(get_image_filename(str(item.id)), item.is_lost) for item in items]
  return Response(
    data={
      'found_items': objects,
      'found_images': images,
    },
  )