from rest_framework import permissions
from django.shortcuts import get_object_or_404

from users.models import CustomUser


class AdminRole(permissions.BasePermission):

    def has_permission(self, request, view):
        cur_user = get_object_or_404(
            CustomUser,
            username=request.user.username)
        return (
            cur_user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    '''Разрешение создания, изменения и удаления только админу.'''

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.role == 'admin')
        )
