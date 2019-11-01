from django.utils.translation import ugettext_lazy as _

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Item, FoundItem
from .serializers import ItemSerializer

class LostItemListView(generics.ListCreateAPIView):
  serializer_class = ItemSerializer

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  def get_queryset(self):
    return Item.objects.filter(user=self.request.user)

class LostItemUpdateView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Item.objects.all()
  serializer_class = ItemSerializer

  def get_queryset(self):
    return Item.objects.filter(user=self.request.user)

@api_view(['POST'])
def addLostItemView(request):
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
    {"detail": _("Added lost item %s." % item.id)},
    status=status.HTTP_201_CREATED
  )
