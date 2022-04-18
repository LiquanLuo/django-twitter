from rest_framework.permissions import BasePermission


class IsObjectOwner(BasePermission):
    """
    Allows access only to authenticated users.
    """

    message = "You do not have permission to access this object"

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return request.user == obj.user