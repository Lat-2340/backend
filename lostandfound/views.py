from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from mongoengine import *

from .models import Item, FoundItem

def indexView(request):
  return HttpResponse('Welcome to lostandfound index.')

@api_view(['POST'])
def addLostItemView(request):
  try:
    item = Item(**request.data)
    item.save()
    print(item.id, item)
  except ValidationError as e:
    return Response({"error": _(str(e))}, status=status.HTTP_400_BAD_REQUEST)
  return Response(
    {"detail": _("Added lost item %s." % item.id)},
    status=status.HTTP_201_CREATED
  )

@api_view(['POST'])
def addFoundItemView(request):
  try:
    item = FoundItem(**request.data)
    item.save()
    print(item.id, item)
  except ValidationError as e:
    return Response(
      {"error": _(str(e))},
      status=status.HTTP_400_BAD_REQUEST
    )
  return Response(
    {"detail": _("Added found item %s." % item.id)},
    status=status.HTTP_201_CREATED
  )
