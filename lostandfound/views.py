from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from mongoengine import *

from .models import Item
from .similarimages import get_similar_image
from . import utils

K = 3
MATCH_THRESHOLD = 0.6

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

    utils.decode_base64(utils.get_image_filename(str(item.id), item.is_lost), img)

    '''
    NOTE:
      matched_info = [[score, item_id], ...] for lost items
      matched_info = [item_id, ...] for found items
    '''
    if item.is_lost: # find the current best matching found images
      similar_img_ids = get_similar_image(str(item.id), "found/", K)
      similar_img_ids.sort(key=lambda x: -x[0]) # descending order
      matched_ids = []

      for score, matched_id in similar_img_ids:
        if score < MATCH_THRESHOLD:
          continue
        try:
          # update match_info of the matched found item
          found_item = Item.objects(id=matched_id, is_lost=False)[0]
          found_item.matched_info.append(matched_id)
          found_item.save()
          print("append found match: ", matched_id, found_item.matched_info)

          matched_ids.append([score, matched_id])
        except:
          continue

    else: # refresh lost matching when adding found image
      similar_img_ids = get_similar_image(str(item.id), "lost/", float("inf"))
      matched_ids = []

      for score, matched_id in similar_img_ids:
        try:
          lost_item = Item.objects(id=matched_id, is_lost=True)[0]
        except:
          print("invalid match id: ", matched_id)
          continue

        if score < MATCH_THRESHOLD:
          continue

        if len(lost_item.matched_info) >= K:
          fscore, fid = lost_item.matched_info[-1] # lowest matching item
          if score > fscore:
            # update match_info of the matched lost item: replace first (lowest matching) match with the current item
            lost_item.matched_info[-1] = [score, str(item.id)]
            print("replace lost match: ", matched_id, lost_item.matched_info)

            # update match_info of the replaced found item
            replace_found_item = Item.objects(id=fid, is_lost=False)[0]
            replace_found_item.matched_info = list(filter(lambda x: x != item.id, replace_found_item.matched_info))
            replace_found_item.save()
            print("updated replaced found item: ", replace_found_item.id, replace_found_item.matched_info)

            matched_ids.append(matched_id)
        else:
          # update match_info of the matched lost item: append the current item
          lost_item.matched_info.append([score, str(item.id)])
          matched_ids.append(matched_id)
          print("append lost match: ", matched_id, lost_item.matched_info)

        lost_item.matched_info.sort(key=lambda x: -x[0]) # descending order
        lost_item.save()

    item.matched_info = matched_ids
    item.save()
    print("Added item: ", item.id, item)

  except (ValidationError, FieldDoesNotExist) as e:
    return Response(
      {"error": str(e)},
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
        {"error": "More than one item with id %s" % request.data['id']},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
    item = item[0]

    data = request.data.dict() # mutable copy of request.data
    if 'image' in data:
      img = data['image']
      del data['image']
      utils.decode_base64(utils.get_image_filename(str(item.id), item.is_lost), img)

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
    {"detail": "Updated item %s." % item.id},
    status=status.HTTP_200_OK
  )

@api_view(['DELETE'])
def deleteItemView(request):
  try:
    item = Item.objects(id=request.data['id'], user=request.user.username)
    if len(item) > 1:
      return Response(
        {"error": "More than one item with id %s" % request.data['id']},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
    item = item[0]

    utils.remove_image_file(item.id, item.is_lost)
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
  print("getUserLostItems: ", items)
  objects = [item.to_json() for item in items]
  images = [utils.encode_base64(utils.get_image_filename(str(item.id), item.is_lost)) for item in items]
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
  images = [utils.encode_base64(utils.get_image_filename(str(item.id), item.is_lost)) for item in items]
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
    lost_id = request.GET['id']
    lost_item = Item.objects(user=username, id=lost_id)

    if len(lost_item) > 1:
      return Response(
        {"error": "More than one item with id %s" % lost_id},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
    lost_item = lost_item[0]

    matched_items, matched_images = [], []
    for _, matched_id in lost_item.matched_info:
      try:
        matched_items.append(Item.objects(id=matched_id)[0].to_json())
        matched_images.append(utils.encode_base64(utils.get_image_filename(matched_id, is_lost=False)))
      except:
        print("invalid match id: ", matched_id)
        continue

    # print("matched items: ", matched_items)
    return Response(
      data={
        'matched_items': matched_items,
        'matched_images': matched_images,
      },
    )

  except (KeyError, ValidationError) as e:
    print(e)
    return Response(
      {"error": str(e)},
      status=status.HTTP_400_BAD_REQUEST
    )