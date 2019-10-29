from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from rest_framework import permissions, generics, views, status
from rest_framework.response import Response

from .serializers import UserSerializer


class UserRegisterView(generics.CreateAPIView):
  model = get_user_model()
  permission_classes = [ permissions.AllowAny ]
  serializer_class = UserSerializer

class TokenDestroyView(views.APIView):
  def post(self, request):
    try:
      request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
      pass
    return Response({"detail": _("Log out success.")}, status=status.HTTP_200_OK)
