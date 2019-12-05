from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from mongoengine import *

from .models import Item
from .similarimages import get_similar_image
from . import utils

K = 3
MATCH_THRESHOLD = 0.6

def match_lost_item(item):
  similar_img_ids = get_similar_image(str(item.id), "found/", K)
  similar_img_ids.sort(key=lambda x: -x[0]) # descending order
  match_ids = []

  for score, match_id in similar_img_ids:
    if score < MATCH_THRESHOLD:
      continue
    try:
      # update match_info of the matched found item
      found_item = Item.objects(id=match_id)[0]
      found_item.match_info.append(match_id)
      found_item.save()
      print("append found match: ", match_id, found_item.match_info)

      match_ids.append([score, match_id])
    except:
      print("failed to append match for: ", match_id)
      continue

  return match_ids

def match_found_item(item):
  similar_img_ids = get_similar_image(str(item.id), "lost/", float("inf"))
  match_ids = []

  for score, match_id in similar_img_ids:
    try:
      lost_item = Item.objects(id=match_id)[0]
    except:
      print("invalid match id: ", match_id)
      continue

    if score < MATCH_THRESHOLD:
      continue

    if len(lost_item.match_info) >= K:
      fscore, fid = lost_item.match_info[-1] # lowest matching item
      if score > fscore:
        # update match_info of the matched lost item: replace first (lowest matching) match with the current item
        lost_item.match_info[-1] = [score, str(item.id)]
        print("replace lost match: ", match_id, lost_item.match_info)

        # update match_info of the replaced found item
        replace_found_item = Item.objects(id=fid)[0]
        replace_found_item.match_info = list(filter(lambda x: x != item.id, replace_found_item.match_info))
        replace_found_item.save()
        print("updated replaced found item: ", replace_found_item.id, replace_found_item.match_info)

        match_ids.append(match_id)
    else:
      # update match_info of the matched lost item: append the current item
      lost_item.match_info.append([score, str(item.id)])
      match_ids.append(match_id)
      print("append lost match: ", match_id, lost_item.match_info)

    lost_item.match_info.sort(key=lambda x: -x[0]) # descending order
    lost_item.save()

  return match_ids

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
      match_info = [[score, item_id], ...] for lost items
      match_info = [item_id, ...] for found items
    '''
    if item.is_lost: # find the current best matching found images
      match_ids = match_lost_item(item)
    else: # refresh lost matching when adding found image
      match_ids = match_found_item(item)

    item.match_info = match_ids
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

# get match_id for lost and found item respectively
def get_match_id(match):
  return match if len(match) == 1 else match[-1]

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

    for match in item.match_info:
      match_id = get_match_id(match)
      try:
        match_item = Item.objects(id=match_id)[0]
        match_item.match_info = list(filter(lambda x: get_match_id(x) != item.id, match_item.match_info))
        print("delete match: ", match_id, match_item.match_info)
        if match_item.is_lost: # rematch for lost item
          match_item.match_info = match_lost_item(match_item)
        match_item.save()
      except:
        print("failed to delete match for: ", match_id)
        continue

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

    match_items, match_images = [], []
    for _, match_id in lost_item.match_info:
      try:
        match_items.append(Item.objects(id=match_id)[0].to_json())
        match_images.append(utils.encode_base64(utils.get_image_filename(match_id, is_lost=False)))
      except:
        print("invalid match id: ", match_id)
        continue

    # print("matched items: ", match_items)
    return Response(
      data={
        'match_items': match_items,
        'match_images': match_images,
      },
    )

  except (KeyError, ValidationError) as e:
    print(e)
    return Response(
      {"error": str(e)},
      status=status.HTTP_400_BAD_REQUEST
    )