from rest_framework import permissions

class canUpdate(permissions.BasePermission):
  ''' Custom permission to only allow users to update their own CustomUser record. '''

  def has_object_permission(self, request, view, obj):
    return obj.username == request.user.username and \
      ('username' not in request.data or obj.username == request.data['username'])