from rest_framework import permissions
from pprint import pprint


class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    '''Custom Permission Usage.
    Allow all methods for admin or just read_only methods to normal users.'''
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin