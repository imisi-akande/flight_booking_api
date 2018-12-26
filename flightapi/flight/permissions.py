from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Set object level permission in order to restrict access to owners of the issue alone.
    """

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        else:
            return False