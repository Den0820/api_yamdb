from rest_framework import permissions
from django.shortcuts import get_object_or_404

from users.models import CustomUser


class OwnerOrAdmins(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or request.user.is_admin
            or request.user.is_superuser)


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
                and request.user.is_admin)
        )


class IsOwnerOrReadOnlyReview(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.author == request.user
               or request.user.is_admin
               or request.user.is_moder)
