from rest_framework import permissions
from users.models import CustomUser
from django.shortcuts import get_object_or_404


class AdminRole(permissions.BasePermission):

    def has_permission(self, request, view):
        cur_user = get_object_or_404(CustomUser, username=request.user.username)
        return (
            cur_user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    '''Разрешение создания, изменения и удаления только админу.'''

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.user.role == 'admin')