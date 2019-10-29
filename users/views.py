from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.db import connections

from rest_framework import permissions, generics, views, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserSerializer


class UserRegisterView(generics.CreateAPIView):
  ''' View for user registration '''
  model = get_user_model()
  permission_classes = [ permissions.AllowAny ]
  serializer_class = UserSerializer

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
def get_user_offices_view(request):
  ''' Returns list of office info matched with user organization '''
  with connections['default'].cursor() as cursor:
    cursor.execute("SELECT * FROM PickupLocation WHERE org_id = %s", [request.user.org.orgname])
    return Response(dictfetchall(cursor))