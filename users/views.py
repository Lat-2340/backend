from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.db import connections

from rest_framework import permissions, generics, views, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .serializers import UserSerializer
from .models import CustomUser
from .permissions import IsOwner

class UserRegisterView(generics.CreateAPIView):
  ''' View for user registration '''
  model = get_user_model()
  permission_classes = [ permissions.AllowAny ] # override the default permission
  serializer_class = UserSerializer

class UserUpdateView(generics.RetrieveUpdateDestroyAPIView):
  queryset = CustomUser.objects.all()
  permission_classes = [ IsOwner ]
  serializer_class = UserSerializer

  # TODO forbit updating other's record

class TokenDestroyView(views.APIView):
  ''' View for user token expiration / logout '''
  def post(self, request):
    try:
      request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
      pass
    return Response({"detail": _("Log out success.")}, status=status.HTTP_200_OK)

def dictfetchall(cursor):
  ''' Helper function: return all rows from a cursor as a dict '''
  columns = [col[0] for col in cursor.description]
  return [ dict(zip(columns, row)) for row in cursor.fetchall() ]

@api_view(['GET'])
def getPickupLocationsView(request):
  ''' Return list of pickup locations matched with user organization '''
  with connections['default'].cursor() as cursor:
    cursor.execute("SELECT * FROM PickupLocation WHERE org_id = %s", [request.user.org.orgname])
    return Response(dictfetchall(cursor))

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def getOrganizationsView(request):
  ''' Return list of organizations '''
  with connections['default'].cursor() as cursor:
    cursor.execute("SELECT * FROM Organization")
    return Response(dictfetchall(cursor))