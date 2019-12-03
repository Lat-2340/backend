from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from mongoengine import *

from .models import Item
from .utils import encode_base64, decode_base64, get_image_filename, get_id_from_image_filename
from .similarimages import get_similar_image


@api_view(['POST'])
def addItemView(request):
  try:
    data = request.data.dict() # mutable copy of request.data

    if 'image' not in data:
      return Response(
        {"error": "An image of the item is required"},
        status=status.HTTP_400_BAD_REQUEST
      )

    img = data['image']
    del data['image']

    item = Item(**data)
    item.user = request.user.username
    item.save()

    decode_base64(get_image_filename(str(item.id), item.is_lost), img)

    if item.is_lost: # find the current best matching found images
      similar_found_imgs = get_similar_image(str(item.id), "found/", K=3) # [[score, filename], []]
      for img_info in similar_found_imgs:
        img_info[1] = get_id_from_image_filename(img_info[1])
      similar_found_imgs.sort(key=lambda x:x[0])
      item.matched_info = similar_found_imgs

    else: # refresh lost matching when adding found image
      similar_lost_imgs = get_similar_image(str(item.id), "lost/", K=float("inf"))

      for score, img_file in similar_lost_imgs:
        lost_item = Item.objects(id=get_id_from_image_filename(img_file), is_lost=True)
        fscore, _ = lost_item.matched_info[0]
        if score > fscore:
          lost_item.matched_info[0] = [score, item.id]
          lost_item.matched_info.sorted(key=lambda x:x[0])

    item.save()
    print("Added item: ", item.id, item)

  except (ValidationError, FieldDoesNotExist) as e:
    return Response(
      {"error": _(str(e))},
      status=status.HTTP_400_BAD_REQUEST
    )
  return Response(
    {"detail": "Added item %s." % item.id},
    status=status.HTTP_201_CREATED
  )

@api_view(['POST'])
def updateItemView(request):
  try:
    item = Item.objects(id=request.data['id'], user=request.user.username)
    if len(item) > 1:
      return Response(
        {"error": "More than one item found with id %s" % request.data['id']},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
    item = item[0]

    data = request.data.dict() # mutable copy of request.data
    if 'image' in data:
      img = data['image']
      del data['image']
      decode_base64(get_image_filename(str(item.id), item.is_lost), img)

    for k, v in data.items():
      item[k] = v

    item.save()
    print("Updated item: ", item.id, item)

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
        {"error": "More than one item found with id %s" % request.data['id']},
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
      {"error": str(e)},
      status=status.HTTP_400_BAD_REQUEST
    )
  return Response(
    {"detail": "Deleted item %s." % item.id},
    status=status.HTTP_204_NO_CONTENT
  )

@api_view(['GET'])
def getUserLostItems(request):
  username = request.user.username
  items = Item.objects(user=username, is_lost=True)
  objects = [item.to_json() for item in items]
  images = [encode_base64(get_image_filename(str(item.id), item.is_lost)) for item in items]
  return Response(
    data={
      'lost_items': objects,
      'lost_images': images,
    },
  )

@api_view(['GET'])
def getUserFoundItems(request):
  username = request.user.username
  items = Item.objects(user=username, is_lost=False)
  objects = [item.to_json() for item in items]
  images = [encode_base64(get_image_filename(str(item.id), item.is_lost)) for item in items]
  return Response(
    data={
      'found_items': objects,
      'found_images': images,
    },
  )

@api_view(['GET'])
def getMatchedFoundItems(request):
  try:
    username = request.user.username
    lost_id = request.data['id']
    lost_item = Item.objects(user=username, id=lost_id)

    matched_items, matched_images = [], []
    for matched_id in lost_item.matched_ids:
      matched_items.append(Item.objects(id=matched_id)[0])
      matched_images = encode_base64(get_image_filename(matched_id, is_lost=False))

    return Response(
      data={
        'matched_items': matched_items,
        'matched_images': matched_images,
      },
    )

  except (KeyError, IndexError) as e:
    return Response(
      {"error": str(e)},
      status=status.HTTP_400_BAD_REQUEST
    )